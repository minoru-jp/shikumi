# Shikumi API

Public APIs on the Shikumi semantic-system object.

related: [Core Semantics](../specification/core.md)

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

related: [CORE_007](../specification/core.md#core_007)

name: Shikumi

kind: Type


### `recognizes()`

```python
def recognizes(self, information_type: InformationType[Any]) -> bool
```

Returns whether this Shikumi recognizes the Information Type by identity.

name: recognizes()

kind: Operation

input: information_type: InformationType[Any]

output: bool


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

```python
from shikumi import InformationType, Shikumi, attach_information

Title = InformationType("title", str)
InternalId = InformationType("internal-id", int)

class Page:
    pass

attach_information(Page, Title, "Overview")
attach_information(Page, InternalId, 42)

docs = Shikumi(information_types=[Title])
assert docs.recognizes(Title)
assert not docs.recognizes(InternalId)

item = docs.view(Page).focused
assert item.values(Title) == ("Overview",)
assert not item.has(InternalId)
```

related: [CORE_004](../specification/core.md#core_004), [CORE_008](../specification/core.md#core_008)

name: view()

kind: Operation

input: subject: object | Focus, placement: tuple[str, ...] | None = None

output: SemanticView


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

name: derive_structure_specification()

kind: Operation

input: subject: object | Focus, placement: tuple[str, ...] | None = None

output: StructureSpecification


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


related: [CORE_005](../specification/core.md#core_005), [VAL_005](../specification/validation.md#val_005), [CORE_008](../specification/core.md#core_008)

name: validate()

kind: Operation

input: subject: object | Focus, placement: tuple[str, ...] | None = None, structure_specification: StructureSpecification | None = None

output: ValidationResult

---
