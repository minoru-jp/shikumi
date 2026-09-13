# Shikumi API Reference

This document defines Shikumi's public API and its semantic contracts.

[`glossary.md`](./glossary.md) contains the canonical concept definitions. This document defines how those concepts are exposed as Python APIs. If the two differ in their conceptual meaning, `glossary.md` takes precedence.

Modules, classes, functions, and attributes not documented here are treated as internal implementation details. The public API is provided from `shikumi` and `shikumi.standard`.

This API specification may be defined ahead of the implementation. Public implementations are expected to conform to this document.

## Basic contracts

Shikumi operates on objects and information established after Python execution. It does not reconstruct semantic state by interpreting Python source as an AST.

Information is not owned by a Shikumi instance. The specification side attaches information to Python runtime objects through Information Attachment, and a Shikumi includes only the Information Types it recognizes in its Semantic Views.

The concrete form of a Descriptor is not restricted by the public API. Descriptors may use decorators, `@=`, docstrings, ordinary function calls, or any other runtime processing. Descriptor Uses and Information Attachments are separate runtime facts. When needed, the specification side records a use with `record_descriptor_use()` and attaches information with `attach_information()`.

Validation operates on Semantic Views, and Realizers generate Artifacts from Semantic Views. Realizers are not owned by Shikumi.

---

# Core API: `shikumi`

## Information

### `Cardinality`

```python
class Cardinality(str, Enum):
    ONE = "one"
    MANY = "many"
```

Represents the number of Information values allowed by an Information Type.

`ONE` represents a semantically singular value, but Information Attachment itself does not reject an invalid state. Multiple values may remain attached and later be diagnosed as nonconforming by a Validation Rule.

### `InformationType`

```python
class InformationType(Generic[T]):
    name: str
    value_type: type[T] | tuple[type[Any], ...]
    cardinality: Cardinality
```

Defines an Information Type. When a single `value_type` is specified, that Python type is also propagated as the type variable `T` for static typing.

Information Types are identified by object identity. Two `InformationType` objects with the same `name` are still distinct Information Types.

The constructor validates that `name` is a non-empty `str`, `value_type` is a `type` or a non-empty `tuple[type, ...]` usable as the second argument to `isinstance()`, and `cardinality` is a `Cardinality`. Invalid type declarations are rejected immediately rather than deferred to a later `accepts()` call.

#### Attributes

```python
name: str
value_type: type[T] | tuple[type[Any], ...]
cardinality: Cardinality
```

#### `accepts(value)`

```python
def accepts(self, value: object) -> bool
```

Returns whether `value` conforms to `value_type`. This checks only the value type; it does not validate cardinality or any other condition.

An Information Type does not special-case values that happen to be another entity, a `module`, a function, or another Python object. Shikumi does not perform reference resolution or reachability analysis for such values. Their meaning is defined by the specification side.

### `Information`

```python
@dataclass(frozen=True)
class Information(Generic[T]):
    type: InformationType[T]
    value: T
    subject: object
```

Represents one item of Information attached to a runtime object. The fact that a Descriptor was used is not embedded in `Information`; it is recorded separately as a `DescriptorUse`.

### `attach_information()`

```python
def attach_information(
    subject: object,
    information_type: InformationType[T],
    value: T,
) -> Information[T]
```

**The standard path for Information Attachment.**

Attaches `value` to `subject` as Information of `information_type` and returns the resulting `Information`.

This function is not description syntax. It is a low-level API used by the specification side when defining custom Descriptors.

`attach_information()` itself does not validate:

- conformance to `value_type`;
- conformance to `cardinality`; or
- whether a Shikumi recognizes the Information Type.

These conditions are validated by the necessary Validation Rules after the semantic state has been preserved.

`subject` must be a weak-referenceable runtime object. A subject that cannot be attached to raises `TypeError`.

The Information registry is managed by runtime identity rather than `subject.__eq__` or `subject.__hash__`. Internal registry records do not directly hold `subject`; public `Information` objects are assembled when `information_of()` is called. The registry itself therefore does not directly hold a strong reference to `subject`. However, if an internal value corresponding to `Information.value`, or another Python object reachable from that value, references `subject`, that reference may extend the lifetime of `subject`. Shikumi does not weaken or sever reference relationships held by information values themselves.

### `information_of()`

```python
def information_of(subject: object) -> tuple[Information[Any], ...]
```

Returns Information directly attached to `subject`, in attachment order.

It does not filter by the Information Types recognized by a Shikumi or interpret semantic structure.

### `clear_information()`

```python
def clear_information(subject: object) -> None
```

Removes Information directly attached to `subject`.

This API is mainly intended for tests, interactive tools, and cases that explicitly manage runtime lifecycles. It is not intended for ordinary specification or description code.

## Descriptor Uses

### `DescriptorUse`

```python
@dataclass(frozen=True)
class DescriptorUse:
    descriptor: object
    subject: object
```

Represents the fact that a Descriptor was used on a runtime object. This is independent from Information Attachment: a single Descriptor Use may perform zero, one, or multiple Information Attachments.

### `record_descriptor_use()`

```python
def record_descriptor_use(
    subject: object,
    descriptor: object,
) -> DescriptorUse
```

Low-level API that records that `descriptor` was used on `subject`. It does not track the Descriptor's import source or source-level name; the supplied Python object is treated by runtime identity. Bound methods are matched by the same bound instance and underlying function, so accessing `writer.describe` again still identifies the same Descriptor.

### `descriptor_uses_of()` / `clear_descriptor_uses()`

```python
def descriptor_uses_of(subject: object) -> tuple[DescriptorUse, ...]
def clear_descriptor_uses(subject: object) -> None
```

Retrieve or remove Descriptor Uses recorded directly on the target. `clear_descriptor_uses()` is mainly intended for tests and explicit runtime lifecycle management.

Like the Information registry, the Descriptor Use registry is managed by runtime identity rather than the target's `__eq__` or `__hash__`. Internal records do not directly hold the target; public `DescriptorUse` objects are assembled when retrieved, so the registry itself does not directly hold a strong reference to the target. However, if a recorded `descriptor`, or another Python object reachable from it, references the target, that reference may extend the target's lifetime. A bound method, for example, normally retains its instance. Shikumi does not weaken or sever reference relationships held by Descriptors themselves.

### `StructureSelector`

```python
StructureSelector(
    *,
    kind: StructuralKind | None = None,
    at: tuple[str, ...] | None = None,
    under: tuple[str, ...] | None = None,
)
```

Selects structural positions targeted by a Descriptor Use Rule. `kind` selects a structural kind, `at` requires an exact match with one effective path, and `under` selects the given path itself and everything below it. `at` and `under` cannot be specified together. A selector with no conditions matches every position. To allow multiple candidate positions, selectors can be OR-composed with `StructureSelector.one_of(a, b, ...)` or `a | b`.

#### `one_of()` / `|`

```python
@classmethod
def one_of(
    cls,
    *selectors: StructureSelector,
) -> StructureSelector
```

Returns a selector that matches when any supplied selector matches. `a | b` has the same meaning as `StructureSelector.one_of(a, b)`.

Paths are evaluated relative to the same specification root used by Structure Specifications. When an entire package is the Focus, the package itself is the root `()`. When `placement` is supplied for a standalone module, the intended placement is used as its effective path.

### `DescriptorUseRule`

```python
DescriptorUseRule(
    descriptor: object,
    allowed: StructureSelector,
    recommended: StructureSelector | None = None,
    name: str | None = None,
)
```

Defines where one Descriptor is allowed or recommended in structure. A use outside `allowed` is an error. A use that matches `allowed` but not `recommended` is a warning. With `recommended=None`, all positions within the allowed range are treated equally.

A Descriptor with no rule is not structurally constrained by this mechanism. Shikumi does not infer an implicit use range from an Information Type, information value, import source, or similar data.

## Class binding for `@=`

### `class_binding()`

```python
def class_binding(
    value: T,
    connect: Callable[[type, T], None],
) -> object
```

Low-level API for applying processing after a class has been created when the target class does not yet exist during execution of its class body.

It is intended for authors of custom `@=` Descriptors. Shikumi does not interpret the type or meaning of `value`; it only guarantees that `connect(subject, value)` is called after the class has been created.

The returned object can receive consecutive `@=` operations under the same name.

```python
class Tags:
    def __init__(self, information_type: InformationType) -> None:
        self.information_type = information_type

    def __imatmul__(self, value: str):
        return class_binding(value, self._connect)

    def _connect(self, subject: type, value: str) -> None:
        record_descriptor_use(subject, self)
        attach_information(
            subject,
            self.information_type,
            value,
        )


tags = Tags(Tag)

class Page:
    tags @= "python"
    tags @= "runtime"
```

`class_binding()` only provides the timing for post-class-creation processing. It does not require Descriptor Use recording or Information Attachment. When using it to implement a Shikumi Descriptor, call `record_descriptor_use()` and `attach_information()` from `connect` as needed.

The internal implementation technique used by `class_binding()` is not part of the public contract.

---
## Structure and Focus

### `Focus`

```python
@dataclass(frozen=True)
class Focus:
    subject: object
    placement: tuple[str, ...] | None = None
```

Represents the Focus used to construct a Semantic View. `placement` is an optional position that explicitly states where the subject should be interpreted as being placed in structure. `None` means that no placement is specified; the empty tuple `()` explicitly represents the root of a Structure Specification.

In ordinary cases, a runtime object can be passed directly to `Shikumi.view(subject)` or `Shikumi.validate(subject)`. Placement must be specified when validating a standalone module. When Validation Rules are applied to a child module during validation of an entire package, its placement is inherited from the resolved structure.

### `StructuralKind`

```python
class StructuralKind(str, Enum):
    PACKAGE = "package"
    MODULE = "module"
    ENTITY = "entity"
```

The structural kinds represented by Core.

### `StructureNode`

```python
@dataclass(frozen=True)
class StructureNode:
    subject: object
    kind: StructuralKind
    name: str
    path: tuple[str, ...]
    parent: object | None = None
```

Represents one position in semantic structure.

`subject` is the runtime object and `path` is its structural position. `parent` may contain the parent runtime object.

### `ResolvedStructure`

```python
@dataclass(frozen=True)
class ResolvedStructure:
    focus: Focus
    nodes: tuple[StructureNode, ...]
```

Semantic structure resolved for one Focus.

#### `node_for(subject)`

```python
def node_for(self, subject: object) -> StructureNode | None
```

Returns the node whose subject matches by identity.

`ResolvedStructure` validates structural invariants when it is created. At minimum, it requires the Focus subject to occur exactly once, every `path` to be unique, every `subject` to be unique by identity, every node to be under the Focus root, and every non-Focus path to have a structural parent path. A custom `Structure` cannot return a `ResolvedStructure` that violates these invariants.

### `Structure`

```python
class Structure(ABC):
    @abstractmethod
    def resolve(self, focus: Focus) -> ResolvedStructure:
        ...
```

Abstract base class for interpreting Structure.

A custom Structure implements `resolve()` and returns a `ResolvedStructure` containing the Focus.

### `PythonStructure`

```python
PythonStructure()
```

The minimal Python Structure provided by Core. `PythonStructure` treats classes as `StructuralKind.ENTITY`; functions and methods are not included as entities.

- When a `class` is the Focus, only that entity is interpreted.
- When a `module` is the Focus, the module and classes defined in that module are interpreted. Lexically nested classes defined inside classes are also included recursively as entities.
- A `package` is recognized as a package, but child modules are not imported implicitly.
- Imported external classes are not treated as entities of the importing module.
- A class defined elsewhere and merely assigned to a class attribute as an alias is not treated as a nested entity.
- When `Focus.placement` is specified, the resolved structural path is relocated to that position without changing the identity of the runtime object.

### `StructureElement`

```python
@dataclass(frozen=True)
class StructureElement:
    path: tuple[str, ...]
    kind: StructuralKind
```

Represents a structural kind required at a root-relative path in a Structure Specification. The root itself uses the path `()`.

### `StructureSpecification`

```python
StructureSpecification(elements: Iterable[StructureElement])
```

Represents a Structure Specification as a set of root-relative `StructureElement`s. Element paths must be unique, the root element `()` must exist, and every element's parent path must exist.

Current structure checking is exact: both missing required elements and additional elements not present in the specification are errors.

A specification body can explicitly expose a `StructureSpecification` as an ordinary Python object. When a Structure Specification is obtained from another description body, it is still represented as the same `StructureSpecification` type. Shikumi does not automatically switch between these two acquisition methods.

#### `from_resolved()`

```python
@classmethod
def from_resolved(
    cls,
    structure: ResolvedStructure,
) -> StructureSpecification
```

Derives a Structure Specification from a resolved structure, using its Focus as the root `()`.

#### `element_at()` / `subtree()`

```python
def element_at(self, path: tuple[str, ...]) -> StructureElement | None
def subtree(self, placement: tuple[str, ...]) -> tuple[StructureElement, ...]
```

Returns the element at the given position or the subtree at and below the given position.

---

## Semantic Views

### `ViewItem`

```python
@dataclass(frozen=True)
class ViewItem:
    node: StructureNode
    information: tuple[Information[Any], ...]
    descriptor_uses: tuple[DescriptorUse, ...] = ()
```

Represents one interpretation target included in a Semantic View.

#### `subject`

```python
@property
def subject(self) -> object
```

Returns `node.subject`.

#### `kind`

```python
@property
def kind(self) -> StructuralKind
```

Returns `node.kind`.

#### `records(information_type)`

```python
def records(
    self,
    information_type: InformationType[T],
) -> tuple[Information[T], ...]
```

Returns Information selected by identity for the specified Information Type.

#### `values(information_type)`

```python
def values(
    self,
    information_type: InformationType[T],
) -> tuple[T, ...]
```

Returns values of the specified Information Type in attachment order.

It always returns a tuple because multiple values may exist before validation even for a single-valued Information Type.

The type variable of `InformationType[T]` propagates through `records()` and `values()`. For example, if a static type checker interprets `Title = InformationType("title", str)` as `InformationType[str]`, then `item.values(Title)` is `tuple[str, ...]`. Shikumi distributes `py.typed`, and this type relationship from Core Information Types through retrieval is part of the public contract.

When multiple Python types are specified as `value_type=(str, int)`, the current contract does not guarantee that the type variable is inferred as a precise union. Full propagation of `T` into Standard's `assignment()` / `decorator()` or arbitrary custom Descriptors is also outside this first-stage contract. Descriptor APIs are not made more complex solely for typing at the expense of runtime flexibility.

#### `has(information_type)`

```python
def has(self, information_type: InformationType[T]) -> bool
```

Returns whether at least one item of Information of the specified Information Type is present.

#### `uses(descriptor)`

```python
def uses(self, descriptor: object) -> tuple[DescriptorUse, ...]
```

Returns uses of the specified Descriptor recorded on this target. Bound methods are matched by the same bound instance and underlying function.

### `SemanticView`

```python
@dataclass(frozen=True)
class SemanticView:
    focus: Focus
    structure: ResolvedStructure
    items: tuple[ViewItem, ...]
```

A Semantic View constructed for one Focus.

#### `focused`

```python
@property
def focused(self) -> ViewItem
```

Returns the `ViewItem` corresponding to the Focus itself.

#### `entities`

```python
@property
def entities(self) -> tuple[ViewItem, ...]
```

Returns items corresponding to entities.

#### `modules`

```python
@property
def modules(self) -> tuple[ViewItem, ...]
```

Returns items corresponding to modules.

#### `packages`

```python
@property
def packages(self) -> tuple[ViewItem, ...]
```

Returns items corresponding to packages.

#### `item(subject)`

```python
def item(self, subject: object) -> ViewItem
```

Returns the `ViewItem` whose subject matches by identity. Raises `UnknownViewSubjectError` if the subject is not present in the Semantic View.

#### `subview(subject)`

```python
def subview(self, subject: object) -> SemanticView
```

Uses a subject already contained in this Semantic View as a new Focus and returns a partial Semantic View from its structural subtree. It reuses the original `ResolvedStructure`, Information, and Descriptor Uses and does not reinterpret the Python runtime. Passing the original Focus itself returns the same `SemanticView`. A subject not present in the Semantic View raises `UnknownViewSubjectError`.

`SemanticView` is iterable and yields `ViewItem`s in `items` order.

---

## Shikumi

### `Shikumi`

```python
Shikumi(
    *,
    structure: Structure | None = None,
    information_types: Iterable[InformationType[Any]] = (),
    validators: Iterable[ValidationRule] = (),
    descriptor_rules: Iterable[DescriptorUseRule] = (),
)
```

Composes a Structure, recognized Information Types, Validation Rules, and Descriptor Use Rules into one semantic system.

When `structure=None`, `PythonStructure()` is used. An explicitly supplied `structure` must be a `Structure` instance. Custom structural interpretation can be implemented by subclassing `Structure`.

Each element of `information_types`, `validators`, and `descriptor_rules` must respectively be an `InformationType`, `ValidationRule`, or `DescriptorUseRule`. The same object must not be registered more than once in the same Shikumi. Components of the wrong kind cause `TypeError`; duplicates cause `ValueError`.

The constructor guarantees only component kinds and local registration invariants. It does not attempt `Structure.resolve()`, pre-evaluate semantic consistency among Validation Rules, or determine whether Descriptor Use Rules are reachable in the actual Structure. These concerns remain runtime responsibilities of the individual components so that constructor validation does not restrict the expressive power of custom extensions.

### `recognizes()`

```python
def recognizes(self, information_type: InformationType[Any]) -> bool
```

Returns whether this Shikumi recognizes the Information Type by identity.

### `view()`

```python
def view(
    self,
    subject: object | Focus,
    *,
    placement: tuple[str, ...] | None = None,
) -> SemanticView
```

Interprets the target as the Focus and returns a Semantic View. When `placement` is specified, that position is used as the Focus's structural placement. If a `Focus` already contains a placement, a method argument must not specify another placement on top of it.

Only Information whose Information Type is recognized in this Shikumi's `information_types` is included in the Semantic View. Unrecognized Information attached to a target is not deleted; it simply does not appear in that view. Descriptor Uses are included independently of Information Types, and only uses relevant to `descriptor_rules` are checked against structure.

### `derive_structure_specification()`

```python
def derive_structure_specification(
    self,
    subject: object | Focus,
    *,
    placement: tuple[str, ...] | None = None,
) -> StructureSpecification
```

Interprets a description body using this Shikumi's `Structure` and derives a Structure Specification rooted at its Focus. This method does not search for an explicitly defined Structure Specification. It is used when the caller explicitly chooses to derive one from a description body.

### `validate()`

```python
def validate(
    self,
    subject: object | Focus,
    *,
    placement: tuple[str, ...] | None = None,
    structure_specification: StructureSpecification | None = None,
) -> ValidationResult
```

Constructs a Semantic View with the target as the Focus and evaluates applicable Validation Rules and `descriptor_rules`. If `structure_specification` is supplied, conformance to that Structure Specification is checked in the same validation operation.

When `validate()` is called on a standalone module, `placement` is required. The current import path is not implicitly adopted as the intended placement. When Validation Rules are applied to child modules while validating an entire package, placement is inherited automatically from the resolved structure.

Validation Rules requiring a particular `StructuralKind` are applied not only to the root Focus but also to each structural element contained in the Semantic View. For a child element, validation receives a partial Semantic View cut from the initially constructed view using `SemanticView.subview()`. A single `validate()` call does not repeatedly invoke `Structure.resolve()` or retrieve Information and Descriptor Uses again; the runtime state interpreted once is shared throughout the validation operation.

When matching a Structure Specification, if the Focus has a placement, only the subtree at and below that position is matched strictly. This prevents standalone module validation from behaving as though sibling modules outside the module had been observed.

---

## Validation

### `DiagnosticSeverity`

```python
class DiagnosticSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
```

Severity of a Diagnostic.

### `Diagnostic`

```python
Diagnostic(
    message: str,
    code: str | None = None,
    severity: DiagnosticSeverity = DiagnosticSeverity.ERROR,
    subject: object | None = None,
)
```

One Diagnostic. `message`, `code`, and `severity` are type-checked at construction, and `severity` must be a `DiagnosticSeverity` itself. Strings such as `"error"` are not converted implicitly.

When a Validation Rule returns a Diagnostic with `subject=None`, the Focus of the Semantic View passed to that rule is set automatically as the `subject`.

### `ValidationRule`

```python
ValidationRule(
    focus_kind: StructuralKind,
    check: Callable[[SemanticView], ValidationOutput],
    name: str,
)
```

One Validation Rule.

`ValidationRule` objects are distinguished by identity. Construction validates that `focus_kind` is a `StructuralKind`, `check` is callable, and `name` is a non-empty `str`.

When called, a rule requires a Semantic View whose Focus matches `focus_kind` and returns a tuple of Diagnostics.

### `validator()`

```python
def validator(
    *,
    focus: StructuralKind,
    name: str | None = None,
) -> Callable[[ValidationFunction], ValidationRule]
```

Helper decorator for defining a `ValidationRule` from an ordinary Python function.

A validation function receives a `SemanticView` and may return any of the following:

```python
None
Diagnostic
Iterable[Diagnostic]
```

Example:

```python
@validator(focus=StructuralKind.ENTITY)
def require_title(view):
    if not view.focused.has(Title):
        yield Diagnostic(
            "title is required",
            code="title.required",
        )
```

### `check_descriptor_uses()`

```python
def check_descriptor_uses(
    view: SemanticView,
    rules: Iterable[DescriptorUseRule],
) -> tuple[Diagnostic, ...]
```

Checks Descriptor Uses recorded in a Semantic View against Descriptor Use Rules and returns Diagnostics. `Shikumi.validate()` performs this check automatically for registered `descriptor_rules`.

### `StructureCheck` / `check_structure()`

```python
@dataclass(frozen=True)
class StructureCheck:
    specification: StructureSpecification
    placement: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]


def check_structure(
    structure: ResolvedStructure,
    specification: StructureSpecification,
) -> StructureCheck
```

Represents the result of matching a resolved Structure against a Structure Specification. If the Focus has a `placement`, the corresponding subtree is matched; otherwise the root of the Structure Specification is matched.

`StructureCheck.is_valid` is `True` when there are no error Diagnostics.

### `ValidationResult`

```python
@dataclass(frozen=True)
class ValidationResult:
    view: SemanticView
    diagnostics: tuple[Diagnostic, ...]
    structure_check: StructureCheck | None = None
```

The result of one validation operation. When a Structure Specification is supplied, its match result is retained in `structure_check`, and structural Diagnostics are also included in `diagnostics`.

#### `is_valid`

```python
@property
def is_valid(self) -> bool
```

`True` when there are no `ERROR` Diagnostics.

`bool(result)` has the same meaning as `result.is_valid`.

---

## Realization

### `RealizationCheck`

```python
@dataclass(frozen=True)
class RealizationCheck:
    view: SemanticView
    diagnostics: tuple[Diagnostic, ...] = ()
```

The result of asking whether a particular Realizer can realize a Semantic View without generating an Artifact. `is_realizable` is `True` when there are no error Diagnostics. This is independent of conformance to the specification.

### `Realizer`

```python
class Realizer(ABC, Generic[ArtifactT]):
    def check(self, view: SemanticView) -> RealizationCheck:
        ...

    @abstractmethod
    def realize(self, view: SemanticView) -> ArtifactT:
        ...
```

Abstract base class for generating an Artifact from a Semantic View. `check()` asks whether the supplied Semantic View is realizable without generating an Artifact. A Realizer with realization requirements overrides `check()` and returns unmet requirements as `Diagnostic`s. The default implementation treats the view as having no additional realization requirements.

A Realizer does not own a Shikumi and is not owned by a Shikumi. Multiple Realizers may be applied to the same Semantic View.

```python
view = docs.view(source)

markdown = MarkdownRealizer().realize(view)
json_data = JsonRealizer().realize(view)
```

Shikumi does not restrict the Artifact type.

---

## Exceptions

### `ShikumiError`

Base class for exceptions defined by Shikumi.

### `UnsupportedFocusError`

```python
class UnsupportedFocusError(ShikumiError, TypeError):
    ...
```

Raised when a Structure cannot interpret the supplied Focus.

### `UnknownViewSubjectError`

```python
class UnknownViewSubjectError(ShikumiError, LookupError):
    ...
```

Raised when `SemanticView.item()` is asked for a subject that is not present in the Semantic View.

---

# Defining Descriptors

Shikumi does not prescribe the concrete form of a Descriptor. Authors of specification bodies define Descriptors with ordinary Python and perform Information Attachment from within them.

## Decorators without arguments

```python
Kind = InformationType(
    "kind",
    str,
    cardinality=Cardinality.MANY,
)


class KindDescriptions:
    def attr(self, subject):
        """An entity treated as an attribute."""
        record_descriptor_use(subject, self.attr)
        attach_information(
            subject,
            Kind,
            "attr",
        )
        return subject

    def service(self, subject):
        """An entity treated as a service."""
        record_descriptor_use(subject, self.service)
        attach_information(
            subject,
            Kind,
            "service",
        )
        return subject


kind = KindDescriptions()
```

A description body uses these as ordinary Python decorators.

```python
@kind.attr
class Owner:
    pass


@kind.service
class UserService:
    pass
```

Because `attr` and `service` are ordinary Python methods, IDE features such as go-to-definition, docstring display, and type annotations remain available in the usual way.

## Decorators with arguments

```python
Uses = InformationType(
    "uses",
    type,
    cardinality=Cardinality.MANY,
)


class RelationDescriptions:
    def uses(self, target: type):
        """A relationship indicating use of the target entity."""

        def decorate(subject):
            record_descriptor_use(subject, self.uses)
            attach_information(
                subject,
                Uses,
                target,
            )
            return subject

        return decorate


relation = RelationDescriptions()
```

```python
@relation.uses(UserRepository)
class UserService:
    pass
```

Arguments, return values, and decorator construction are the responsibility of the Descriptor author. Shikumi does not wrap them or infer Information from signatures.

## Custom `@=` Descriptors

At the time `@=` is evaluated, the class being described does not yet exist. Use `class_binding()` to perform Information Attachment after the class has been created.

```python
Tag = InformationType(
    "tag",
    str,
    cardinality=Cardinality.MANY,
)


class TagDescriptions:
    def __imatmul__(self, value: str):
        return class_binding(value, self._connect)

    def _connect(self, subject: type, value: str) -> None:
        record_descriptor_use(subject, self)
        attach_information(
            subject,
            Tag,
            value,
        )


tag = TagDescriptions()
```

```python
class UserService:
    tag @= "application"
    tag @= "users"
```

Shikumi does not interpret the type or structure of `value`. The Descriptor author decides what types `@=` accepts and under which Information Type those values are attached.

### Descriptor Use Rule example

```python
endpoint_rule = DescriptorUseRule(
    descriptor=kind.service,
    allowed=StructureSelector(kind=StructuralKind.ENTITY),
    recommended=StructureSelector(
        kind=StructuralKind.ENTITY,
        under=("api",),
    ),
    name="kind.service",
)

system = Shikumi(
    information_types=[Kind],
    descriptor_rules=[endpoint_rule],
)
```

This rule allows `kind.service` only on entities and recommends its use below `api` under the specification root. Use on an entity outside `api` produces a warning; use on anything other than an entity produces an error.

---

# Standard API: `shikumi.standard`

Standard provides reusable concrete functionality composed from Core's public API. Standard does not introduce a new semantic model.

## `assignment()`

```python
def assignment(information_type: InformationType)
```

Returns a standard `@=` Descriptor that attaches the supplied value unchanged as Information of the specified Information Type. A Descriptor Use is also recorded when it is used.

```python
Title = InformationType("title", str)
title = assignment(Title)

class Page:
    title @= "Overview"
```

Consecutive `@=` operations under the same name are supported.

## `decorator()`

```python
def decorator(information_type: InformationType)
```

Returns a simple decorator-producing Descriptor that attaches the supplied value unchanged as Information of the specified Information Type. A Descriptor Use is also recorded when the decorator is applied.

```python
Kind = InformationType("kind", str)
kind = decorator(Kind)

@kind("service")
class Service:
    pass
```

When vocabulary names themselves should remain directly traceable in an IDE, or arguments need custom meaning, define an ordinary Python decorator in the specification body instead of using this convenience function.

## `DocstringWriter` / `docstring()`

```python
DocstringWriter(
    information_type: InformationType,
    *,
    clean: bool = True,
    required: bool = False,
)
```

```python
def docstring(
    information_type: InformationType,
    *,
    clean: bool = True,
    required: bool = False,
) -> DocstringWriter
```

A standard Descriptor that attaches the explicitly applied target's `__doc__` as Information. A Descriptor Use is recorded when it is applied, so the fact that the Descriptor was used remains even when no docstring exists.

```python
Content = content_type()
content = docstring(Content)

@content
class Overview:
    """Overview document."""
```

With `clean=True`, excess indentation is removed according to Python's docstring-cleaning rules.

With `required=False`, nothing is attached when no docstring exists. Required presence of Information is generally best expressed as a Validation Rule.

## `content_type()`

```python
def content_type(
    name: str = "content",
    *,
    value_type: type | tuple[type, ...] = str,
) -> InformationType
```

Convenience function that creates a single-valued Information Type representing primary content.

## `PackageTreeStructure`

```python
PackageTreeStructure()
```

When an already imported package is the Focus, explores its physical package tree, imports child packages and modules through Python's ordinary import mechanism, and constructs semantic structure.

When a module or entity is the Focus, it performs the same local interpretation as `PythonStructure`. In each module, lexically nested classes are included in semantic structure as entities in addition to classes directly under the module.

This Structure treats the results of Python imports as authoritative semantic state. It does not parse source as an AST.

## `information_type_rule()`

```python
def information_type_rule(
    information_type: InformationType,
    *,
    focus: StructuralKind = StructuralKind.ENTITY,
) -> ValidationRule
```

Creates a standard Validation Rule that checks the following for one Information Type:

- multiple values for `Cardinality.ONE`; and
- values that do not conform to `value_type`.

It does not require Information to be present or assign specification-specific meaning to values.

---

# Public API Layers

Core and Standard are divided as follows.

```text
Core (`shikumi`)
├─ Information Types and Information
├─ Information Attachment
├─ low-level post-class-creation binding
├─ Structure, Focus, and Semantic Views
├─ Shikumi
├─ Validation
└─ Realization

Standard (`shikumi.standard`)
├─ generic `@=` Descriptor
├─ generic decorator Descriptor
├─ docstring Descriptor
├─ standard Information Type helpers
├─ package-tree Structure
└─ standard Validation Rules
```

Purpose-specific vocabulary such as `kind`, `attr`, and `rel` is not Standard's responsibility. A specification body defines the vocabulary it needs using ordinary Python definitions.

---

# Behavioral Boundaries

Shikumi assumes ordinary Python class creation and import / execution behavior.

If a user or specification body uses custom decorators, metaclasses, base classes, mixins, or similar mechanisms, Shikumi does not provide compatibility handling for their interactions. If such combinations change Python's standard class-creation process or the execution order of Descriptors, the resulting behavior is not guaranteed.

Shikumi does not perform:

- semantic reconstruction by parsing Python source ASTs;
- automatic Information inference from Descriptor function signatures or return values;
- automatic registration of specific vocabulary;
- automatic deletion of unrecognized Information;
- automatic correction of invalid states before Validation; or
- registration or ownership of Realizers by Shikumi.

These boundaries allow specification authors to define description mechanisms freely with ordinary Python while Shikumi concentrates on semantic interpretation after Information Attachment.

---

# CLI: `shikumi`

Shikumi provides a thin CLI that wires together a `Shikumi` exposed by a specification body, a Python object used as a description body, and an independent Realizer at runtime.

The CLI does not manage registration, discovery, or ownership relationships among specification bodies, description bodies, and Realizers. It loads the supplied Python references through ordinary imports and processes them in place.

Python references use the following forms:

```text
module
module:object
module:outer.inner
```

`--shikumi` and `--realizer` require `module:object`. `--body` may use `module` when the module or package itself is the target, or `module:object` when an entity is the Focus.

## `validate`

```bash
shikumi validate \
  --shikumi SPEC_MODULE:SHIKUMI \
  --body DESCRIPTION_MODULE[:OBJECT] \
  [--at PLACEMENT] \
  [--structure-spec SPEC_MODULE:STRUCTURE | --structure-from DESCRIPTION_MODULE[:OBJECT]] \
  [--realizer REALIZER_MODULE:REALIZER] \
  [--format text|json]
```

Validates the specified description body or entity using `Shikumi.validate()`.

When a standalone module is supplied to `--body`, `--at` is required. Its value is a dotted path such as `api.users` representing the intended structural placement; `.` represents the root of the Structure Specification. Placement may be omitted when an entire package is supplied.

When using a Structure Specification, the user explicitly chooses one of the following:

- `--structure-spec MODULE:OBJECT`: use a `StructureSpecification` exposed directly as a Python object by a specification body or another module. If the specified object does not exist or has the wrong type, this is a CLI configuration error; the CLI does not fall back to derivation from the description body.
- `--structure-from MODULE[:OBJECT]`: interpret the specified description body with the current Shikumi and derive a `StructureSpecification` from its Structure.

When `--realizer` is supplied, the CLI calls `Realizer.check()` in addition to ordinary Validation and asks about Realizability without generating an Artifact. Conformance to the specification and Realizability are kept as separate results in the JSON response. If either contains an error, the command-level `ok` is `false`.

The command returns exit code `0` when both Validation and, when requested, the Realizability check contain no errors; otherwise it returns `1`. Warnings and informational Diagnostics alone still result in `0`.

`validate` does not generate an Artifact.

## `realize`

```bash
shikumi realize \
  --shikumi SPEC_MODULE:SHIKUMI \
  --body DESCRIPTION_MODULE[:OBJECT] \
  [--at PLACEMENT] \
  --realizer REALIZER_MODULE:REALIZER \
  --output PATH \
  [--format text|json]
```

Constructs a Semantic View from the specified description body, passes it to the specified `Realizer`, and generates an Artifact. When `--at` is supplied, that structural placement is reflected in the Semantic View.

`realize` does not implicitly run Validation or `Realizer.check()`. Conformance to the specification, asking about Realizability, and performing Realization are independent operations. Run `validate --realizer ...` first when those checks are needed.

Artifacts that the CLI can write directly to a file are limited to:

- `str`: written as UTF-8 text;
- `bytes` / bytes-like: written as binary; or
- JSON-serializable Python values: written as UTF-8 JSON.

A Realizer that returns another Artifact type cannot be used directly through the CLI's standard output contract.

## `--format`

```text
text
json
```

The default is `text`.

`--format` controls **the CLI's own response format**. It does not control the format of the Artifact generated by a Realizer.

`text` emits formatted text intended for terminal reading.

`json` emits a structured response to stdout for use by LLMs, CI, and other tools. The JSON response includes `format_version`; the current version is `1`.

Example:

```json
{
  "format_version": 1,
  "command": "validate",
  "ok": false,
  "shikumi": "api_spec:api",
  "body": "my_api",
  "focus_kind": "package",
  "placement": null,
  "diagnostic_counts": {
    "error": 1,
    "warning": 0,
    "info": 0
  },
  "diagnostics": [
    {
      "severity": "error",
      "code": "endpoint.path.required",
      "message": "endpoint path is required",
      "subject": "my_api.users.GetUser"
    }
  ],
  "structure": null,
  "realization": null
}
```

When `--output` is supplied during Realization, the Artifact is written to that file and stdout contains only the CLI response. This separation prevents a JSON Artifact from being mixed with a `--format json` CLI response.

Failures the CLI can handle during import, Interpretation, Validation, Realization, or Artifact writing are reported in `json` mode as structured responses with `ok: false` and `error.type` / `error.message`.
