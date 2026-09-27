# Information API

Public APIs for Information Types and runtime Information Attachment.

related: [Description Semantics](../specification/description.md)

## Information

### `Cardinality`

```python
class Cardinality(str, Enum):
    ONE = "one"
    MANY = "many"
```

Represents the number of Information values allowed by an Information Type.

`ONE` represents a semantically singular value, but Information Attachment itself does not reject an invalid state. Multiple values may remain attached and later be diagnosed as nonconforming by a Validation Rule.

name: Cardinality

kind: Type


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

related: [DESC_001](../specification/description.md#desc_001)

name: InformationType

kind: Type


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

name: accepts(value)

kind: Operation

input: value: object

output: bool


### `Information`

```python
@dataclass(frozen=True)
class Information(Generic[T]):
    type: InformationType[T]
    value: T
    subject: object
```

Represents one item of Information attached to a runtime object. The fact that a Descriptor was used is not embedded in `Information`; it is recorded separately as a `DescriptorUse`.

name: Information

kind: Type


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

Example:

```python
from shikumi import (
    InformationType,
    attach_information,
    clear_information,
    information_of,
)

Title = InformationType("title", str)

class Page:
    pass

assert Title.accepts("Overview")
assert not Title.accepts(42)

record = attach_information(Page, Title, "Overview")
assert record.subject is Page
assert tuple(item.value for item in information_of(Page)) == ("Overview",)

clear_information(Page)
assert information_of(Page) == ()
```

The Information registry is managed by runtime identity rather than `subject.__eq__` or `subject.__hash__`. Internal registry records do not directly hold `subject`; public `Information` objects are assembled when `information_of()` is called. The registry itself therefore does not directly hold a strong reference to `subject`. However, if an internal value corresponding to `Information.value`, or another Python object reachable from that value, references `subject`, that reference may extend the lifetime of `subject`. Shikumi does not weaken or sever reference relationships held by information values themselves.

related: [DESC_002](../specification/description.md#desc_002)

name: attach_information()

kind: Operation

input: subject: object, information_type: InformationType[T], value: T

output: Information[T]


### `information_of()`

```python
def information_of(subject: object) -> tuple[Information[Any], ...]
```

Returns Information directly attached to `subject`, in attachment order.

It does not filter by the Information Types recognized by a Shikumi or interpret semantic structure.

name: information_of()

kind: Operation

input: subject: object

output: tuple[Information[Any], ...]


### `clear_information()`

```python
def clear_information(subject: object) -> None
```

Removes Information directly attached to `subject`.

This API is mainly intended for tests, interactive tools, and cases that explicitly manage runtime lifecycles. It is not intended for ordinary specification or description code.

name: clear_information()

kind: Operation

input: subject: object

output: None
