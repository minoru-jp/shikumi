# Semantic View API

Public APIs for reading SemanticView and ViewItem objects.

related: [Core Semantics](../specification/core.md)

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

name: ViewItem

kind: Type


#### `subject`

```python
@property
def subject(self) -> object
```

Returns `node.subject`.

name: subject

kind: Value


#### `kind`

```python
@property
def kind(self) -> StructuralKind
```

Returns `node.kind`.

name: kind

kind: Value


#### `records(information_type)`

```python
def records(
    self,
    information_type: InformationType[T],
) -> tuple[Information[T], ...]
```

Returns Information selected by identity for the specified Information Type.

name: records(information_type)

kind: Operation

input: information_type: InformationType[T]

output: tuple[Information[T], ...]


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

name: values(information_type)

kind: Operation

input: information_type: InformationType[T]

output: tuple[T, ...]


#### `has(information_type)`

```python
def has(self, information_type: InformationType[T]) -> bool
```

Returns whether at least one item of Information of the specified Information Type is present.

name: has(information_type)

kind: Operation

input: information_type: InformationType[Any]

output: bool


#### `uses(descriptor)`

```python
def uses(self, descriptor: object) -> tuple[DescriptorUse, ...]
```

Returns uses of the specified Descriptor recorded on this target. Bound methods are matched by the same bound instance and underlying function.

name: uses(descriptor)

kind: Operation

input: descriptor: object

output: tuple[DescriptorUse, ...]


### `SemanticView`

```python
@dataclass(frozen=True)
class SemanticView:
    focus: Focus
    structure: ResolvedStructure
    items: tuple[ViewItem, ...]
```

A Semantic View constructed for one Focus.

```python
from shikumi import InformationType, Shikumi, UnknownViewSubjectError, attach_information

Title = InformationType("title", str)

class Page:
    pass

attach_information(Page, Title, "Overview")
view = Shikumi(information_types=[Title]).view(Page)

assert view.focused.values(Title) == ("Overview",)
assert view.focused.has(Title)
assert view.item(Page) is view.focused
assert view.subview(Page) is view

class Other:
    pass

try:
    view.item(Other)
except UnknownViewSubjectError:
    pass
else:
    raise AssertionError("unknown subjects must be rejected")
```

related: [CORE_008](../specification/core.md#core_008)

name: SemanticView

kind: Type


#### `focused`

```python
@property
def focused(self) -> ViewItem
```

Returns the `ViewItem` corresponding to the Focus itself.

name: focused

kind: Value


#### `entities`

```python
@property
def entities(self) -> tuple[ViewItem, ...]
```

Returns items corresponding to entities.

name: entities

kind: Value


#### `modules`

```python
@property
def modules(self) -> tuple[ViewItem, ...]
```

Returns items corresponding to modules.

name: modules

kind: Value


#### `packages`

```python
@property
def packages(self) -> tuple[ViewItem, ...]
```

Returns items corresponding to packages.

name: packages

kind: Value


#### `item(subject)`

```python
def item(self, subject: object) -> ViewItem
```

Returns the `ViewItem` whose subject matches by identity. Raises `UnknownViewSubjectError` if the subject is not present in the Semantic View.

name: item(subject)

kind: Operation

input: subject: object

output: ViewItem


#### `subview(subject)`

```python
def subview(self, subject: object) -> SemanticView
```

Uses a subject already contained in this Semantic View as a new Focus and returns a partial Semantic View from its structural subtree. It reuses the original `ResolvedStructure`, Information, and Descriptor Uses and does not reinterpret the Python runtime. Passing the original Focus itself returns the same `SemanticView`. A subject not present in the Semantic View raises `UnknownViewSubjectError`.

`SemanticView` is iterable and yields `ViewItem`s in `items` order.


related: [CORE_008](../specification/core.md#core_008)

name: subview(subject)

kind: Operation

input: subject: object

output: SemanticView

---
