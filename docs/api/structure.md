# Structure API

Public APIs for structural interpretation, Focus, and StructureSpecification.

related: [Structure Semantics](../specification/structure.md)

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

related: [STRUCT_002](../specification/structure.md#struct_002), [STRUCT_003](../specification/structure.md#struct_003)

name: Focus

kind: Type


### `StructuralKind`

```python
class StructuralKind(str, Enum):
    PACKAGE = "package"
    MODULE = "module"
    ENTITY = "entity"
```

The structural kinds represented by Core.

name: StructuralKind

kind: Type


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

name: StructureNode

kind: Type


### `ResolvedStructure`

```python
@dataclass(frozen=True)
class ResolvedStructure:
    focus: Focus
    nodes: tuple[StructureNode, ...]
```

Semantic structure resolved for one Focus.

name: ResolvedStructure

kind: Type


#### `node_for(subject)`

```python
def node_for(self, subject: object) -> StructureNode | None
```

Returns the node whose subject matches by identity.

`ResolvedStructure` validates structural invariants when it is created. At minimum, it requires the Focus subject to occur exactly once, every `path` to be unique, every `subject` to be unique by identity, every node to be under the Focus root, and every non-Focus path to have a structural parent path. A custom `Structure` cannot return a `ResolvedStructure` that violates these invariants.

name: node_for(subject)

kind: Operation

input: subject: object

output: StructureNode | None


### `Structure`

```python
class Structure(ABC):
    @abstractmethod
    def resolve(self, focus: Focus) -> ResolvedStructure:
        ...
```

Abstract base class for interpreting Structure.

A custom Structure implements `resolve()` and returns a `ResolvedStructure` containing the Focus.

name: Structure

kind: Type


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

```python
from types import ModuleType

from shikumi import Focus, PythonStructure, StructureSpecification, StructuralKind

module = ModuleType("demo")
exec(
    "class Service:\n"
    "    class Handler:\n"
    "        pass\n",
    module.__dict__,
)

resolved = PythonStructure().resolve(Focus(module, placement=("app",)))
assert tuple(node.path for node in resolved.nodes) == (
    ("app",),
    ("app", "Service"),
    ("app", "Service", "Handler"),
)

specification = StructureSpecification.from_resolved(resolved)
assert tuple((element.path, element.kind) for element in specification.elements) == (
    ((), StructuralKind.MODULE),
    (("Service",), StructuralKind.ENTITY),
    (("Service", "Handler"), StructuralKind.ENTITY),
)
```

related: [STRUCT_001](../specification/structure.md#struct_001)

name: PythonStructure

kind: Type


### `StructureElement`

```python
@dataclass(frozen=True)
class StructureElement:
    path: tuple[str, ...]
    kind: StructuralKind
    required: bool = True
```

Represents an exact structural element with a concrete name in a Structure Specification. `path` is root-relative and the root itself is `()`.

`required=True` requires the element to exist whenever its parent regulation is active. `required=False` activates the regulation only when that concrete name exists. When an optional exact element is present, the exact regulation still takes precedence over a Logical Structure Element. The root `()` must always be required.

A `StructureElement` path does not embed wildcards or the logical name of a Logical Structure Element. The existing `elements`, `element_at()`, `subtree()`, and `from_resolved()` APIs retain these exact-path semantics in 0.2.0.

related: [STRUCT_007](../specification/structure.md#struct_007), [STRUCT_015](../specification/structure.md#struct_015)

name: StructureElement

kind: Type

### `StructureFragment`

```python
StructureFragment(
    elements: Iterable[StructureElement],
    *,
    logical_elements: Iterable[LogicalStructureElement] = (),
    mounts: Iterable[StructureMount] = (),
    groups: Iterable[StructureGroup] = (),
)
```

Represents a Structure Fragment. A fragment is a self-contained regulation with a root element at `()`. It can be mounted at concrete positions for reuse, or used as the same regulation applied to every concrete instance of a Logical Structure Element.

A normal fragment is closed: descendants not described by the fragment are not allowed.

related: [STRUCT_008](../specification/structure.md#struct_008), [STRUCT_012](../specification/structure.md#struct_012)

name: StructureFragment

kind: Type

#### `unconstrained()`

```python
@classmethod
def unconstrained(cls, kind: StructuralKind) -> StructureFragment
```

Returns a fragment that regulates only the root `StructuralKind` and imposes no structural constraints on descendants.

A closed fragment with no child rules and an unconstrained fragment are deliberately different. The former describes a leaf; only the latter accepts arbitrary descendants.

related: [STRUCT_012](../specification/structure.md#struct_012)

name: unconstrained()

kind: Operation

input: kind: StructuralKind

output: StructureFragment

#### `at()`

```python
def at(self, path: tuple[str, ...]) -> StructureMount
```

Returns a `StructureMount` that reuses this fragment at a concrete path.

name: at()

kind: Operation

input: path: tuple[str, ...]

output: StructureMount

#### `recursive()`

```python
def recursive(
    self,
    *,
    parent: tuple[str, ...] = (),
    logical_name: str,
    names: Iterable[str] | None = None,
    max_count: int | None = None,
) -> StructureFragment
```

Returns a fragment that can reapply itself as a logical child with the same `StructuralKind`. Recursive children have an implicit minimum count of zero, and the regulation is reapplied only to depths actually observed in the finite runtime structure. `names` and `max_count` apply independently at each recursive parent.

related: [STRUCT_017](../specification/structure.md#struct_017)

name: recursive()

kind: Operation

input: parent: tuple[str, ...] = (), logical_name: str, names: Iterable[str] | None = None, max_count: int | None = None

output: StructureFragment

### `StructureMount`

```python
@dataclass(frozen=True)
class StructureMount:
    path: tuple[str, ...]
    fragment: StructureFragment
```

An authoring object that reuses a Structure Fragment at the position of a concrete `StructureElement`. The mount target must already exist as an exact element, and its `StructuralKind` must match the fragment root kind.

Exact elements from the mounted fragment are expanded into `StructureSpecification.elements`, so existing exact lookup APIs retain their original meaning.

related: [STRUCT_008](../specification/structure.md#struct_008)

name: StructureMount

kind: Type

### `LogicalStructureElement`

```python
LogicalStructureElement(
    *,
    parent: tuple[str, ...],
    logical_name: str,
    fragment: StructureFragment,
    names: Iterable[str] | None = None,
    min_count: int = 1,
    max_count: int | None = None,
)
```

Represents a Logical Structure Element. Among concrete children directly below `parent`, children not first resolved by an explicit `StructureElement` are governed by the same `fragment` when they bind to this logical element.

With `names=None`, concrete names are unrestricted. When `names` is supplied, only the enumerated names may bind. `min_count` and `max_count` constrain how many concrete instances may resolve to the logical element under one parent.

A parent cannot define multiple Logical Structure Elements for the same `StructuralKind`. Logical rules for different kinds, such as one for packages and one for modules, may coexist and are selected by the observed kind. Shikumi intentionally does not dispatch different regulations through prefixes, suffixes, globs, regular expressions, or arbitrary predicates.

related: [STRUCT_009](../specification/structure.md#struct_009), [STRUCT_010](../specification/structure.md#struct_010), [STRUCT_011](../specification/structure.md#struct_011)

name: LogicalStructureElement

kind: Type

### `StructureGroup`

```python
StructureGroup(
    *,
    parent: tuple[str, ...],
    members: Iterable[str],
    min_count: int = 0,
    max_count: int | None = None,
)
```

Constrains the aggregate presence count of different exact `StructureElement` siblings. Every member must name an exact child directly below `parent`. Each member retains its own kind, optionality, and mounted fragment; the group only constrains how many members are present and never selects a regulation.

For example, `min_count=1, max_count=1` means exactly one of the listed exact siblings must exist.

related: [STRUCT_018](../specification/structure.md#struct_018)

name: StructureGroup

kind: Type

### `StructureSpecification`

```python
StructureSpecification(
    elements: Iterable[StructureElement],
    *,
    logical_elements: Iterable[LogicalStructureElement] = (),
    mounts: Iterable[StructureMount] = (),
    groups: Iterable[StructureGroup] = (),
)
```

Represents a Structure Specification. `elements` remains a set of exact `StructureElement`s: paths must be unique, the root `()` and every parent path must be defined. The root is always required, while child exact elements may be optional with `required=False`.

When an optional exact element is absent, required children and logical cardinality within that subtree are not evaluated. When it is present, the subtree becomes active and its descendant regulations are checked normally.

`mounts` reuses Structure Fragments at concrete positions. `logical_elements` adds Logical Structure Elements whose concrete instance names are not necessarily fixed. `groups` adds aggregate cardinality across exact siblings. An explicit exact element, even when optional, always takes precedence over a logical element that could otherwise accept the same name.

The exact semantics of `elements`, `element_at()`, `subtree()`, and `from_resolved()` are unchanged from 0.1.x. Logical names are not written into `ResolvedStructure` actual paths; they are recorded as bindings during structure checking.

```python
from shikumi import (
    LogicalStructureElement,
    StructuralKind,
    StructureElement,
    StructureFragment,
    StructureSpecification,
)

actor = StructureFragment(
    [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("GUI",), StructuralKind.PACKAGE),
    ]
)

specification = StructureSpecification(
    [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
        StructureElement(
            ("INTERACTION", "NON_SWDESC"),
            StructuralKind.PACKAGE,
            required=False,
        ),
    ],
    logical_elements=[
        LogicalStructureElement(
            parent=("INTERACTION",),
            logical_name="actor",
            fragment=actor,
            min_count=0,
        )
    ],
    mounts=[
        StructureFragment.unconstrained(StructuralKind.PACKAGE).at(
            ("INTERACTION", "NON_SWDESC")
        )
    ],
)

assert specification.element_at(("INTERACTION", "NON_SWDESC")) is not None
assert specification.logical_elements[0].logical_name == "actor"
```

Logical rules by kind, recursive fragments, and group cardinality can be composed independently.

```python
from shikumi import (
    LogicalStructureElement,
    StructuralKind,
    StructureElement,
    StructureFragment,
    StructureGroup,
    StructureSpecification,
)

module = StructureFragment([StructureElement((), StructuralKind.MODULE)])
package_tree = StructureFragment(
    [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("LOCAL",), StructuralKind.PACKAGE, required=False),
        StructureElement(("REMOTE",), StructuralKind.PACKAGE, required=False),
    ],
    logical_elements=[
        LogicalStructureElement(
            parent=(),
            logical_name="module",
            fragment=module,
            min_count=0,
        )
    ],
    groups=[
        StructureGroup(
            parent=(),
            members=("LOCAL", "REMOTE"),
            min_count=0,
            max_count=1,
        )
    ],
).recursive(logical_name="package")

specification = StructureSpecification(
    [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("src",), StructuralKind.PACKAGE),
    ],
    mounts=[package_tree.at(("src",))],
)

assert specification.element_at(("src", "LOCAL")) is not None
assert specification.groups[0].max_count == 1
```

related: [STRUCT_004](../specification/structure.md#struct_004), [STRUCT_007](../specification/structure.md#struct_007), [STRUCT_009](../specification/structure.md#struct_009), [STRUCT_013](../specification/structure.md#struct_013), [STRUCT_015](../specification/structure.md#struct_015), [STRUCT_016](../specification/structure.md#struct_016), [STRUCT_017](../specification/structure.md#struct_017), [STRUCT_018](../specification/structure.md#struct_018)

name: StructureSpecification

kind: Type

#### `from_resolved()`

```python
@classmethod
def from_resolved(
    cls,
    structure: ResolvedStructure,
) -> StructureSpecification
```

Derives an exact Structure Specification from a resolved Structure, using its Focus as the root `()`. Logical Structure Elements are not inferred from runtime structure alone.

related: [STRUCT_005](../specification/structure.md#struct_005), [STRUCT_007](../specification/structure.md#struct_007)

name: from_resolved()

kind: Operation

input: structure: ResolvedStructure

output: StructureSpecification

#### `element_at()`

```python
def element_at(self, path: tuple[str, ...]) -> StructureElement | None
```

Returns the exact `StructureElement` at the specified position. It does not look up a Logical Structure Element by logical name or by a concrete binding.

related: [STRUCT_007](../specification/structure.md#struct_007)

name: element_at()

kind: Operation

input: path: tuple[str, ...]

output: StructureElement | None

#### `subtree()`

```python
def subtree(self, placement: tuple[str, ...]) -> tuple[StructureElement, ...]
```

Returns exact `StructureElement`s at and below the specified position in specification order. It does not return concrete runtime paths created by Logical Structure Element bindings.

related: [STRUCT_007](../specification/structure.md#struct_007)

name: subtree()

kind: Operation

input: placement: tuple[str, ...]

output: tuple[StructureElement, ...]

---
