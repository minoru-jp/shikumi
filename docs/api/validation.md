# Validation API

Public APIs for Diagnostics, Validation Rules, structural checks, and ValidationResult.

related: [Validation Semantics](../specification/validation.md)

## Validation

### `DiagnosticSeverity`

```python
class DiagnosticSeverity(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
```

Severity of a Diagnostic.

name: DiagnosticSeverity

kind: Type


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

related: [VAL_008](../specification/validation.md#val_008)

name: Diagnostic

kind: Type


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

name: ValidationRule

kind: Type


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
from shikumi import (
    Diagnostic,
    InformationType,
    Shikumi,
    StructuralKind,
    attach_information,
    validator,
)

Title = InformationType("title", str)

@validator(focus=StructuralKind.ENTITY)
def require_title(view):
    if not view.focused.has(Title):
        yield Diagnostic("title is required", code="title.required")

docs = Shikumi(information_types=[Title], validators=[require_title])

class MissingTitle:
    pass

invalid = docs.validate(MissingTitle)
assert not invalid.is_valid
assert invalid.diagnostics[0].code == "title.required"
assert invalid.diagnostics[0].subject is MissingTitle

class Titled:
    pass

attach_information(Titled, Title, "Overview")
assert docs.validate(Titled).is_valid
```

name: validator()

kind: Operation

input: function: Callable[[SemanticView], Diagnostic | Iterable[Diagnostic] | None]

output: ValidationRule


### `check_descriptor_uses()`

```python
def check_descriptor_uses(
    view: SemanticView,
    rules: Iterable[DescriptorUseRule],
) -> tuple[Diagnostic, ...]
```

Checks Descriptor Uses recorded in a Semantic View against Descriptor Use Rules and returns Diagnostics. `Shikumi.validate()` performs this check automatically for registered `descriptor_rules`.

related: [VAL_003](../specification/validation.md#val_003)

name: check_descriptor_uses()

kind: Operation

input: view: SemanticView, rules: Iterable[DescriptorUseRule]

output: tuple[Diagnostic, ...]


### `StructureBinding`

```python
@dataclass(frozen=True)
class StructureBinding:
    logical_element: LogicalStructureElement
    actual_path: tuple[str, ...]
```

Represents the correspondence between a Logical Structure Element and the concrete path that resolved to that regulation during structure checking. The actual paths in `ResolvedStructure` are not rewritten.

related: [STRUCT_013](../specification/structure.md#struct_013)

name: StructureBinding

kind: Type

### `StructureCheck`

```python
@dataclass(frozen=True)
class StructureCheck:
    specification: StructureSpecification
    placement: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    bindings: tuple[StructureBinding, ...] = ()
```

Represents the result of matching a resolved Structure against a Structure Specification. `placement` retains the actual position in the Structure Specification that was checked. When Logical Structure Elements are resolved, `bindings` retains the logical-to-actual correspondences.

related: [VAL_004](../specification/validation.md#val_004), [VAL_007](../specification/validation.md#val_007)

name: StructureCheck

kind: Type

#### `is_valid`

```python
@property
def is_valid(self) -> bool
```

`True` when there are no `ERROR` Diagnostics. `bool(check)` has the same meaning as `check.is_valid`.

name: is_valid

kind: Value

### `check_structure()`

```python
def check_structure(
    structure: ResolvedStructure,
    specification: StructureSpecification,
) -> StructureCheck
```

Matches a resolved Structure against a Structure Specification. If the Focus has a `placement`, only that subtree is matched; otherwise the specification root is matched. Closed exact and logical regulations report missing required elements, kind mismatches, and unspecified additional elements as errors. For an unconstrained Structure Fragment, topology below that fragment root is not checked.

```python
from shikumi import (
    Focus,
    PythonStructure,
    StructuralKind,
    StructureElement,
    StructureSpecification,
    check_structure,
)

class Page:
    pass

resolved = PythonStructure().resolve(Focus(Page))
expected = StructureSpecification(
    [StructureElement(path=(), kind=StructuralKind.ENTITY)]
)
assert check_structure(resolved, expected).is_valid

wrong = StructureSpecification(
    [StructureElement(path=(), kind=StructuralKind.MODULE)]
)
mismatch = check_structure(resolved, wrong)
assert not mismatch.is_valid
assert mismatch.diagnostics[0].code == "structure.kind.mismatch"
```

related: [VAL_004](../specification/validation.md#val_004), [VAL_007](../specification/validation.md#val_007)

name: check_structure()

kind: Operation

input: structure: ResolvedStructure, specification: StructureSpecification

output: StructureCheck

### `ValidationResult`

```python
@dataclass(frozen=True)
class ValidationResult:
    view: SemanticView
    diagnostics: tuple[Diagnostic, ...]
    structure_check: StructureCheck | None = None
```

The result of one validation operation. When a Structure Specification is supplied, its match result is retained in `structure_check`, and structural Diagnostics are also included in `diagnostics`.

related: [VAL_002](../specification/validation.md#val_002)

name: ValidationResult

kind: Type


#### `is_valid`

```python
@property
def is_valid(self) -> bool
```

`True` when there are no `ERROR` Diagnostics.

`bool(result)` has the same meaning as `result.is_valid`.


name: is_valid

kind: Value

---
