# Descriptor API

Covers Descriptor Use recording, structural usage rules, and post-class-creation binding.

related: [Description Semantics](../specification/description.md)

## Descriptor Uses

### `DescriptorUse`

```python
@dataclass(frozen=True)
class DescriptorUse:
    descriptor: object
    subject: object
```

Represents the runtime fact that a Descriptor was used on a subject. It is independent of Information Attachment: one Descriptor Use may attach zero, one, or many Information values.

related: [DESC_003](../specification/description.md#desc_003)

name: DescriptorUse

kind: Type

### `record_descriptor_use()`

```python
def record_descriptor_use(
    subject: object,
    descriptor: object,
) -> DescriptorUse
```

Low-level API that records that `descriptor` was used on `subject`. It does not track the Descriptor's import source or source-level name; the supplied Python object is treated as the runtime identity. Bound methods are matched by bound instance and underlying function, so repeated attribute access such as `writer.describe` identifies the same Descriptor.

name: record_descriptor_use()

kind: Operation

input: subject: object, descriptor: object

output: DescriptorUse

### Descriptor-use registry

Like the Information registry, the Descriptor Use registry identifies subjects by runtime identity rather than `__eq__` or `__hash__`. Internal records do not directly retain the subject; public `DescriptorUse` values are reconstructed on retrieval, so the registry itself does not directly keep the subject alive. A recorded `descriptor`, or another Python object reachable from it, may still retain the subject. For example, a bound method normally retains its instance. Shikumi does not weaken or sever reference relationships owned by the Descriptor itself.

#### `descriptor_uses_of()`

```python
def descriptor_uses_of(subject: object) -> tuple[DescriptorUse, ...]
```

Returns Descriptor Uses directly recorded on the subject, in use order.

name: descriptor_uses_of()

kind: Operation

input: subject: object

output: tuple[DescriptorUse, ...]

#### `clear_descriptor_uses()`

```python
def clear_descriptor_uses(subject: object) -> None
```

Removes Descriptor Uses directly recorded on the subject. This API is mainly useful for tests and explicit runtime-lifecycle management.

name: clear_descriptor_uses()

kind: Operation

input: subject: object

output: None

### `StructureSelector`

```python
StructureSelector(
    *,
    kind: StructuralKind | None = None,
    at: tuple[str, ...] | None = None,
    under: tuple[str, ...] | None = None,
)
```

Selects structural positions targeted by a Descriptor Use Rule. `kind` restricts Structural Kind, `at` requires an exact effective path, and `under` selects a path and all descendants including that path itself. `at` and `under` cannot be specified together. A selector with no fields matches every position. Use `StructureSelector.one_of(a, b, ...)` or `a | b` to combine alternatives.

name: StructureSelector

kind: Type

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

name: one_of()

kind: Operation

input: *selectors: StructureSelector

output: StructureSelector

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

A Descriptor with no rule is not structurally constrained by this mechanism. Shikumi does not infer an implicit use range from an Information Type, Information value, import source, or similar data.

related: [VAL_003](../specification/validation.md#val_003)

name: DescriptorUseRule

kind: Type

## Class binding for `@=`

### `ClassBinding[T]`

```python
class ClassBinding(Protocol[T_contra]):
    def __imatmul__(self, value: T_contra) -> Self: ...
```

Public static typing contract for the temporary value returned by `class_binding()`. It expresses that additional values of the same type as the initial value can be written with `@=` under the same class-body name.

`ClassBinding[T]` is a typing contract. The concrete runtime binding class and its internal state are not part of the public API. Custom Descriptors normally obtain this type from `class_binding()` rather than constructing it directly.

related: [DESC_006](../specification/description.md#desc_006)

name: ClassBinding

kind: Type

### `class_binding()`

```python
def class_binding(
    value: T,
    connect: Callable[[type[object], T], None],
) -> ClassBinding[T]
```

Low-level API for applying processing during class creation, after the class body has finished executing and before `__init_subclass__()`, when the target class did not yet exist while the class body was running. The current implementation realizes this timing through `__set_name__()`.

Authors of custom `@=` Descriptors can use this API, but Shikumi Core does not require `@=` as a Descriptor syntax. Shikumi does not interpret the type or meaning of `value`; it only guarantees that `connect(subject, value)` is called at the timing described above. `connect` must not depend on state added by `__init_subclass__()`. Shikumi does not normalize exceptions raised by `connect`, so the externally visible exception shape follows Python's class-creation semantics. On Python 3.11, exceptions raised from `__set_name__()` are wrapped in `RuntimeError`; on Python 3.12 and later, the original exception is propagated with a runtime note. Consumers should not rely on a version-independent wrapper exception.

The returned object can receive consecutive `@=` operations under the same name.

In the normal authoring flow, the writer held in an outer namespace such as a module is not consumed. A temporary binding is placed under the corresponding name in each class-body namespace. Aliasing the binding object itself or directly reusing it across multiple classes is not part of the public contract.

```python
from shikumi import (
    ClassBinding,
    InformationType,
    attach_information,
    class_binding,
    descriptor_uses_of,
    information_of,
    record_descriptor_use,
)

Tag = InformationType("tag", str)

class Tags:
    def __init__(self, information_type: InformationType[str]) -> None:
        self.information_type = information_type

    def __imatmul__(self, value: str) -> ClassBinding[str]:
        return class_binding(value, self._connect)

    def _connect(self, subject: type[object], value: str) -> None:
        record_descriptor_use(subject, self)
        attach_information(subject, self.information_type, value)

tags = Tags(Tag)

class Page:
    tags @= "python"
    tags @= "runtime"

assert tuple(record.value for record in information_of(Page)) == (
    "python",
    "runtime",
)
assert len(descriptor_uses_of(Page)) == 2
```

`class_binding()` only provides the connection timing during class creation. It does not require Descriptor Use recording or Information Attachment. When using it to implement a Shikumi Descriptor, call `record_descriptor_use()` and `attach_information()` from `connect` as needed.

The internal implementation technique used by `class_binding()` is not part of the public contract.

---

related: [DESC_006](../specification/description.md#desc_006)

name: class_binding()

kind: Operation

input: value: T, connect: Callable[[type[object], T], None]

output: ClassBinding[T]
