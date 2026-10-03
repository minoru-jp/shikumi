"""Structure concepts used to interpret Python runtime objects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from enum import Enum
from types import ModuleType
from typing import cast

from .errors import UnsupportedFocusError


@dataclass(frozen=True, slots=True)
class Focus:
    """The semantic center from which a view is constructed.

    ``placement`` is an optional structural position supplied by the caller.
    It is useful when a module is interpreted independently of the package in
    which it is intended to be placed.  ``None`` means that no placement
    context was supplied; an empty tuple means the root of a structural
    specification was supplied explicitly.
    """

    subject: object
    placement: tuple[str, ...] | None = None

    def __post_init__(self) -> None:
        if self.placement is None:
            return
        if isinstance(self.placement, str):
            raise TypeError("focus placement must be a tuple of path components")
        normalized = tuple(self.placement)
        if any(not isinstance(part, str) or not part for part in normalized):
            raise ValueError("focus placement components must be non-empty strings")
        object.__setattr__(self, "placement", normalized)


class StructuralKind(str, Enum):
    """Kinds currently represented by the core Python structure."""

    PACKAGE = "package"
    MODULE = "module"
    ENTITY = "entity"


@dataclass(frozen=True, slots=True)
class StructureNode:
    """One subject positioned in a resolved semantic structure."""

    subject: object
    kind: StructuralKind
    name: str
    path: tuple[str, ...]
    parent: object | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.kind, StructuralKind):
            raise TypeError("structure node kind must be a StructuralKind")
        if not isinstance(self.name, str):
            raise TypeError("structure node name must be a string")
        if not self.name:
            raise ValueError("structure node name must not be empty")
        if isinstance(self.path, str):
            raise TypeError("structure node path must be a tuple of path components")
        normalized = tuple(self.path)
        if any(not isinstance(part, str) or not part for part in normalized):
            raise ValueError("structure node path components must be non-empty strings")
        object.__setattr__(self, "path", normalized)


@dataclass(frozen=True, slots=True)
class ResolvedStructure:
    """A structure resolved for one focus."""

    focus: Focus
    nodes: tuple[StructureNode, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.focus, Focus):
            raise TypeError("resolved structure focus must be a Focus")
        nodes = tuple(self.nodes)
        object.__setattr__(self, "nodes", nodes)
        if not nodes:
            raise ValueError("resolved structure must contain at least one node")
        if any(not isinstance(node, StructureNode) for node in nodes):
            raise TypeError("resolved structure nodes must be StructureNode objects")

        focus_nodes = [node for node in nodes if node.subject is self.focus.subject]
        if not focus_nodes:
            raise ValueError("resolved structure must contain its focus subject")
        if len(focus_nodes) != 1:
            raise ValueError(
                "resolved structure must contain its focus subject exactly once"
            )
        root = focus_nodes[0]

        seen_paths: set[tuple[str, ...]] = set()
        seen_subjects: set[int] = set()
        for node in nodes:
            if node.path in seen_paths:
                raise ValueError(
                    "resolved structure contains duplicate path: "
                    f"{StructureSpecification.format_path(node.path)}"
                )
            seen_paths.add(node.path)

            identity = id(node.subject)
            if identity in seen_subjects:
                raise ValueError(
                    "resolved structure contains duplicate subject identity"
                )
            seen_subjects.add(identity)

            if node.path[: len(root.path)] != root.path:
                raise ValueError(
                    "resolved structure contains a node outside its focus root"
                )

        paths = {node.path for node in nodes}
        for node in nodes:
            if node is root:
                continue
            if node.path[:-1] not in paths:
                raise ValueError(
                    "resolved structure node path has no parent: "
                    f"{StructureSpecification.format_path(node.path)}"
                )

    def node_for(self, subject: object) -> StructureNode | None:
        for node in self.nodes:
            if node.subject is subject:
                return node
        return None


@dataclass(frozen=True, slots=True)
class StructureElement:
    """One kind at a concrete root-relative structural path.

    ``required`` controls whether the concrete element must exist when its
    parent regulation is active.  Optionality never changes exact-name
    precedence: when an optional exact element exists at runtime, it is still
    matched before any logical child regulation at the same parent.
    """

    path: tuple[str, ...]
    kind: StructuralKind
    required: bool = True

    def __post_init__(self) -> None:
        if isinstance(self.path, str):
            raise TypeError("structure element path must be a tuple of path components")
        normalized = tuple(self.path)
        if any(not isinstance(part, str) or not part for part in normalized):
            raise ValueError(
                "structure element path components must be non-empty strings"
            )
        if not isinstance(self.kind, StructuralKind):
            raise TypeError("structure element kind must be a StructuralKind")
        if not isinstance(self.required, bool):
            raise TypeError("structure element required must be a bool")
        object.__setattr__(self, "path", normalized)


@dataclass(frozen=True, slots=True)
class StructureMount:
    """Mount one reusable structure fragment at a concrete path."""

    path: tuple[str, ...]
    fragment: StructureFragment

    def __post_init__(self) -> None:
        if isinstance(self.path, str):
            raise TypeError("structure mount path must be a tuple of path components")
        normalized = tuple(self.path)
        if any(not isinstance(part, str) or not part for part in normalized):
            raise ValueError(
                "structure mount path components must be non-empty strings"
            )
        if not isinstance(self.fragment, StructureFragment):
            raise TypeError("structure mount fragment must be a StructureFragment")
        object.__setattr__(self, "path", normalized)


@dataclass(frozen=True, slots=True, init=False)
class StructureGroup:
    """Cardinality constraint across exact sibling elements.

    ``members`` names exact children directly below ``parent``.  Group
    membership does not select a regulation; every member keeps its own exact
    :class:`StructureElement` and any mounted fragment.  The group constrains
    only how many of those concrete siblings may be present together.
    """

    parent: tuple[str, ...]
    members: tuple[str, ...]
    min_count: int
    max_count: int | None

    def __init__(
        self,
        *,
        parent: tuple[str, ...],
        members: Iterable[str],
        min_count: int = 0,
        max_count: int | None = None,
    ) -> None:
        if isinstance(parent, str):
            raise TypeError("structure group parent must be a tuple of path components")
        normalized_parent = tuple(parent)
        if any(not isinstance(part, str) or not part for part in normalized_parent):
            raise ValueError(
                "structure group parent components must be non-empty strings"
            )
        if isinstance(members, str):
            raise TypeError(
                "structure group members must be an iterable of names, not a string"
            )
        normalized_members = tuple(members)
        if not normalized_members:
            raise ValueError("structure group members must not be empty")
        if any(not isinstance(name, str) or not name for name in normalized_members):
            raise ValueError("structure group members must be non-empty strings")
        if len(set(normalized_members)) != len(normalized_members):
            raise ValueError("structure group members must be unique")
        if not isinstance(min_count, int) or isinstance(min_count, bool):
            raise TypeError("structure group min_count must be an integer")
        if min_count < 0:
            raise ValueError("structure group min_count must be non-negative")
        if max_count is not None:
            if not isinstance(max_count, int) or isinstance(max_count, bool):
                raise TypeError("structure group max_count must be an integer or None")
            if max_count < 0:
                raise ValueError("structure group max_count must be non-negative")
            if max_count < min_count:
                raise ValueError("structure group max_count must be >= min_count")
        if min_count > len(normalized_members):
            raise ValueError("structure group min_count cannot exceed member count")
        if max_count is not None and max_count > len(normalized_members):
            raise ValueError("structure group max_count cannot exceed member count")

        object.__setattr__(self, "parent", normalized_parent)
        object.__setattr__(self, "members", normalized_members)
        object.__setattr__(self, "min_count", min_count)
        object.__setattr__(self, "max_count", max_count)


@dataclass(frozen=True, slots=True)
class _RecursiveStructureElement:
    parent: tuple[str, ...]
    logical_name: str
    names: tuple[str, ...] | None
    max_count: int | None
    template: StructureFragment | None = None


@dataclass(frozen=True, slots=True, init=False)
class LogicalStructureElement:
    """A logical child whose concrete runtime name may vary.

    A logical element belongs to one concrete parent path.  Concrete children
    not claimed by an explicit :class:`StructureElement` may bind to it.  If
    ``names`` is omitted, every otherwise-unclaimed child name is eligible.
    One parent may define at most one logical element for each structural kind;
    children of different kinds can therefore use different logical rules
    without interpreting their names. Shikumi deliberately does not dispatch
    different regulations by prefixes, regular expressions, or other
    name-pattern rules.
    """

    parent: tuple[str, ...]
    logical_name: str
    fragment: StructureFragment
    names: tuple[str, ...] | None
    min_count: int
    max_count: int | None

    def __init__(
        self,
        *,
        parent: tuple[str, ...],
        logical_name: str,
        fragment: StructureFragment,
        names: Iterable[str] | None = None,
        min_count: int = 1,
        max_count: int | None = None,
    ) -> None:
        if isinstance(parent, str):
            raise TypeError(
                "logical structure element parent must be a tuple of path components"
            )
        normalized_parent = tuple(parent)
        if any(not isinstance(part, str) or not part for part in normalized_parent):
            raise ValueError(
                "logical structure element parent components must be non-empty strings"
            )
        if not isinstance(logical_name, str):
            raise TypeError("logical structure element name must be a string")  # pyright: ignore[reportUnreachable]
        if not logical_name:
            raise ValueError("logical structure element name must not be empty")
        if not isinstance(fragment, StructureFragment):
            raise TypeError(  # pyright: ignore[reportUnreachable]
                "logical structure element fragment must be a StructureFragment"
            )
        if names is None:
            normalized_names = None
        else:
            if isinstance(names, str):
                raise TypeError(
                    "logical structure element names must be an iterable of names, not a string"
                )
            normalized_names = tuple(names)
            if not normalized_names:
                raise ValueError(
                    "logical structure element names must not be empty when provided"
                )
            if any(not isinstance(name, str) or not name for name in normalized_names):
                raise ValueError(
                    "logical structure element names must be non-empty strings"
                )
            if len(set(normalized_names)) != len(normalized_names):
                raise ValueError("logical structure element names must be unique")
        if not isinstance(min_count, int) or isinstance(min_count, bool):
            raise TypeError("logical structure element min_count must be an integer")
        if min_count < 0:
            raise ValueError("logical structure element min_count must be non-negative")
        if max_count is not None:
            if not isinstance(max_count, int) or isinstance(max_count, bool):
                raise TypeError(
                    "logical structure element max_count must be an integer or None"
                )
            if max_count < 0:
                raise ValueError(
                    "logical structure element max_count must be non-negative"
                )
            if max_count < min_count:
                raise ValueError(
                    "logical structure element max_count must be >= min_count"
                )

        object.__setattr__(self, "parent", normalized_parent)
        object.__setattr__(self, "logical_name", logical_name)
        object.__setattr__(self, "fragment", fragment)
        object.__setattr__(self, "names", normalized_names)
        object.__setattr__(self, "min_count", min_count)
        object.__setattr__(self, "max_count", max_count)

    def _accepts_name(self, name: str) -> bool:
        return self.names is None or name in self.names


@dataclass(frozen=True, slots=True, init=False)
class StructureFragment:
    """A reusable, root-relative structural regulation.

    A fragment is self-contained and therefore always contains a root element
    at ``()``.  It may be mounted at concrete paths or used as the regulation
    applied to each instance of a :class:`LogicalStructureElement`.

    Fragments are closed by default: descendants not described by the fragment
    are unexpected.  :meth:`unconstrained` constructs the explicit opposite,
    where the root kind is still regulated but all descendants are accepted.
    """

    elements: tuple[StructureElement, ...]
    logical_elements: tuple[LogicalStructureElement, ...]
    mounts: tuple[StructureMount, ...]
    groups: tuple[StructureGroup, ...]
    _unconstrained_paths: tuple[tuple[str, ...], ...]
    _recursive_elements: tuple[_RecursiveStructureElement, ...]

    def __init__(
        self,
        elements: Iterable[StructureElement],
        *,
        logical_elements: Iterable[LogicalStructureElement] = (),
        mounts: Iterable[StructureMount] = (),
        groups: Iterable[StructureGroup] = (),
    ) -> None:
        self._initialize(
            elements,
            logical_elements=logical_elements,
            mounts=mounts,
            groups=groups,
            recursive_elements=(),
            root_unconstrained=False,
        )

    def _initialize(
        self,
        elements: Iterable[StructureElement],
        *,
        logical_elements: Iterable[LogicalStructureElement],
        mounts: Iterable[StructureMount],
        groups: Iterable[StructureGroup],
        recursive_elements: Iterable[_RecursiveStructureElement],
        root_unconstrained: bool,
    ) -> None:
        base_elements = tuple(elements)
        normalized_logical = tuple(logical_elements)
        normalized_mounts = tuple(mounts)
        normalized_groups = tuple(groups)
        normalized_recursive = tuple(recursive_elements)
        if root_unconstrained and (
            normalized_logical
            or normalized_mounts
            or normalized_groups
            or normalized_recursive
            or len(base_elements) != 1
            or not base_elements
            or base_elements[0].path != ()
        ):
            raise ValueError(
                "an unconstrained structure fragment may contain only its root element"
            )

        (
            expanded_elements,
            expanded_logical,
            expanded_groups,
            unconstrained_paths,
            expanded_recursive,
        ) = _compose_structure_rules(
            base_elements,
            normalized_logical,
            normalized_mounts,
            normalized_groups,
            normalized_recursive,
            root_unconstrained=root_unconstrained,
            owner="structure fragment",
        )
        object.__setattr__(self, "elements", expanded_elements)
        object.__setattr__(self, "logical_elements", expanded_logical)
        object.__setattr__(self, "mounts", normalized_mounts)
        object.__setattr__(self, "groups", expanded_groups)
        object.__setattr__(self, "_unconstrained_paths", unconstrained_paths)
        object.__setattr__(self, "_recursive_elements", expanded_recursive)

    @classmethod
    def unconstrained(cls, kind: StructuralKind) -> StructureFragment:
        """Return a fragment that regulates only the root kind.

        Any descendants below the fragment root are accepted without further
        structural constraints.  This is intentionally distinct from an empty
        closed fragment, which describes a leaf.
        """

        fragment = object.__new__(cls)
        fragment._initialize(
            [StructureElement((), kind)],
            logical_elements=(),
            mounts=(),
            groups=(),
            recursive_elements=(),
            root_unconstrained=True,
        )
        return fragment

    @property
    def _root(self) -> StructureElement:
        for element in self.elements:
            if element.path == ():
                return element
        raise RuntimeError("structure fragment has no root element")

    def at(self, path: tuple[str, ...]) -> StructureMount:
        """Return a mount that reuses this fragment at *path*."""

        return StructureMount(path=path, fragment=self)

    def recursive(
        self,
        *,
        parent: tuple[str, ...] = (),
        logical_name: str,
        names: Iterable[str] | None = None,
        max_count: int | None = None,
    ) -> StructureFragment:
        """Return a fragment that may repeat itself below ``parent``.

        Recursive children always have the fragment root's structural kind and
        have an implicit minimum count of zero. This keeps every finite runtime
        tree satisfiable while allowing the same regulation to repeat to any
        observed depth.
        """

        if isinstance(parent, str):
            raise TypeError(
                "recursive structure parent must be a tuple of path components"
            )
        normalized_parent = tuple(parent)
        if any(not isinstance(part, str) or not part for part in normalized_parent):
            raise ValueError(
                "recursive structure parent components must be non-empty strings"
            )
        if not isinstance(logical_name, str):
            raise TypeError("recursive structure logical_name must be a string")  # pyright: ignore[reportUnreachable]
        if not logical_name:
            raise ValueError("recursive structure logical_name must not be empty")
        if names is None:
            normalized_names = None
        else:
            if isinstance(names, str):
                raise TypeError(
                    "recursive structure names must be an iterable of names, not a string"
                )
            normalized_names = tuple(names)
            if not normalized_names:
                raise ValueError(
                    "recursive structure names must not be empty when provided"
                )
            if any(not isinstance(name, str) or not name for name in normalized_names):
                raise ValueError("recursive structure names must be non-empty strings")
            if len(set(normalized_names)) != len(normalized_names):
                raise ValueError("recursive structure names must be unique")
        if max_count is not None:
            if not isinstance(max_count, int) or isinstance(max_count, bool):
                raise TypeError(
                    "recursive structure max_count must be an integer or None"
                )
            if max_count < 0:
                raise ValueError("recursive structure max_count must be non-negative")
        by_path = {element.path: element for element in self.elements}
        if normalized_parent not in by_path:
            raise ValueError(
                "recursive structure parent is not defined: "
                f"{StructureSpecification.format_path(normalized_parent)}"
            )
        if any(
            normalized_parent[: len(path)] == path for path in self._unconstrained_paths
        ):
            raise ValueError(
                "an unconstrained subtree cannot contain recursive child rules: "
                f"{StructureSpecification.format_path(normalized_parent)}"
            )

        declaration = _RecursiveStructureElement(
            parent=normalized_parent,
            logical_name=logical_name,
            names=normalized_names,
            max_count=max_count,
        )
        clone = object.__new__(StructureFragment)
        object.__setattr__(clone, "elements", self.elements)
        object.__setattr__(clone, "logical_elements", self.logical_elements)
        object.__setattr__(clone, "mounts", self.mounts)
        object.__setattr__(clone, "groups", self.groups)
        object.__setattr__(clone, "_unconstrained_paths", self._unconstrained_paths)
        object.__setattr__(
            clone,
            "_recursive_elements",
            self._recursive_elements + (declaration,),
        )
        _validate_logical_rule_uniqueness(
            clone.elements,
            clone.logical_elements,
            clone._recursive_elements,
        )
        return clone


@dataclass(frozen=True, slots=True, init=False)
class StructureSpecification:
    """A structural regulation rooted at one exact element.

    ``elements`` retain their original exact-path meaning. Exact children may
    be optional through :attr:`StructureElement.required`; optionality controls
    activation, not path identity or precedence. Reusable fragments mounted at
    exact paths are expanded into that exact element set during construction.
    ``logical_elements`` add variable concrete names without changing the
    semantics of :attr:`elements`, :meth:`element_at`, :meth:`subtree`, or
    :meth:`from_resolved`.
    """

    elements: tuple[StructureElement, ...]
    logical_elements: tuple[LogicalStructureElement, ...]
    mounts: tuple[StructureMount, ...]
    groups: tuple[StructureGroup, ...]
    _unconstrained_paths: tuple[tuple[str, ...], ...]
    _recursive_elements: tuple[_RecursiveStructureElement, ...]

    def __init__(
        self,
        elements: Iterable[StructureElement],
        *,
        logical_elements: Iterable[LogicalStructureElement] = (),
        mounts: Iterable[StructureMount] = (),
        groups: Iterable[StructureGroup] = (),
    ) -> None:
        base_elements = tuple(elements)
        normalized_logical = tuple(logical_elements)
        normalized_mounts = tuple(mounts)
        normalized_groups = tuple(groups)
        (
            expanded_elements,
            expanded_logical,
            expanded_groups,
            unconstrained_paths,
            expanded_recursive,
        ) = _compose_structure_rules(
            base_elements,
            normalized_logical,
            normalized_mounts,
            normalized_groups,
            (),
            root_unconstrained=False,
            owner="structure specification",
        )
        object.__setattr__(self, "elements", expanded_elements)
        object.__setattr__(self, "logical_elements", expanded_logical)
        object.__setattr__(self, "mounts", normalized_mounts)
        object.__setattr__(self, "groups", expanded_groups)
        object.__setattr__(self, "_unconstrained_paths", unconstrained_paths)
        object.__setattr__(self, "_recursive_elements", expanded_recursive)

    @classmethod
    def from_resolved(cls, structure: ResolvedStructure) -> StructureSpecification:
        """Derive an exact specification from a resolved description structure."""

        root = structure.node_for(structure.focus.subject)
        if root is None:  # guarded by ResolvedStructure, kept defensive here
            raise ValueError("resolved structure has no focus node")
        root_path = root.path

        elements: list[StructureElement] = []
        for node in structure.nodes:
            if node.path[: len(root_path)] != root_path:
                raise ValueError(
                    "resolved structure contains a node outside its focus root"
                )
            relative = node.path[len(root_path) :]
            elements.append(StructureElement(path=relative, kind=node.kind))
        return cls(elements)

    def element_at(self, path: tuple[str, ...]) -> StructureElement | None:
        """Return the exact element at *path*, if any."""

        normalized = tuple(path)
        for element in self.elements:
            if element.path == normalized:
                return element
        return None

    def subtree(self, placement: tuple[str, ...]) -> tuple[StructureElement, ...]:
        """Return exact elements at or below a root-relative placement."""

        normalized = tuple(placement)
        return tuple(
            element
            for element in self.elements
            if element.path[: len(normalized)] == normalized
        )

    @staticmethod
    def format_path(path: tuple[str, ...]) -> str:
        return ".".join(path) if path else "."


def _logical_rule_kind(
    logical: LogicalStructureElement | _RecursiveStructureElement,
    *,
    owner_root_kind: StructuralKind,
) -> StructuralKind:
    if isinstance(logical, LogicalStructureElement):
        return logical.fragment._root.kind
    if logical.template is None:
        return owner_root_kind
    return logical.template._root.kind


def _validate_logical_rule_uniqueness(
    elements: tuple[StructureElement, ...],
    logical_elements: tuple[LogicalStructureElement, ...],
    recursive_elements: tuple[_RecursiveStructureElement, ...],
) -> None:
    by_path = {element.path: element for element in elements}
    owner_root_kind = by_path[()].kind
    by_parent_kind: dict[tuple[tuple[str, ...], StructuralKind], str] = {}
    for logical in (*logical_elements, *recursive_elements):
        key = (
            logical.parent,
            _logical_rule_kind(logical, owner_root_kind=owner_root_kind),
        )
        if key in by_parent_kind:
            raise ValueError(
                "a structural parent may define at most one logical element per "
                "structural kind: "
                f"{StructureSpecification.format_path(logical.parent)} "
                f"({key[1].value})"
            )
        by_parent_kind[key] = logical.logical_name


def _compose_structure_rules(
    elements: tuple[StructureElement, ...],
    logical_elements: tuple[LogicalStructureElement, ...],
    mounts: tuple[StructureMount, ...],
    groups: tuple[StructureGroup, ...],
    recursive_elements: tuple[_RecursiveStructureElement, ...],
    *,
    root_unconstrained: bool,
    owner: str,
) -> tuple[
    tuple[StructureElement, ...],
    tuple[LogicalStructureElement, ...],
    tuple[StructureGroup, ...],
    tuple[tuple[str, ...], ...],
    tuple[_RecursiveStructureElement, ...],
]:
    if not elements:
        raise ValueError(f"{owner} must contain at least one element")
    if any(not isinstance(element, StructureElement) for element in elements):
        raise TypeError(f"{owner} elements must be StructureElement objects")
    if any(
        not isinstance(element, LogicalStructureElement) for element in logical_elements
    ):
        raise TypeError(
            f"{owner} logical_elements must contain LogicalStructureElement objects"
        )
    if any(not isinstance(mount, StructureMount) for mount in mounts):
        raise TypeError(f"{owner} mounts must contain StructureMount objects")
    if any(not isinstance(group, StructureGroup) for group in groups):
        raise TypeError(f"{owner} groups must contain StructureGroup objects")
    if any(
        not isinstance(element, _RecursiveStructureElement)
        for element in recursive_elements
    ):
        raise TypeError(f"{owner} contains an invalid recursive structure rule")

    expanded_elements = list(elements)
    expanded_logical = list(logical_elements)
    expanded_groups = list(groups)
    expanded_recursive = list(recursive_elements)
    unconstrained_paths: list[tuple[str, ...]] = [()] if root_unconstrained else []

    for mount in mounts:
        by_path = {element.path: element for element in expanded_elements}
        target = by_path.get(mount.path)
        if target is None:
            raise ValueError(
                f"structure mount target is not defined: "
                f"{StructureSpecification.format_path(mount.path)}"
            )
        if target.kind is not mount.fragment._root.kind:
            raise ValueError(
                "structure mount root kind does not match target at "
                f"{StructureSpecification.format_path(mount.path)}: expected "
                f"{target.kind.value}, got {mount.fragment._root.kind.value}"
            )
        if any(mount.path[: len(path)] == path for path in unconstrained_paths):
            raise ValueError(
                "cannot mount a structure fragment inside an unconstrained subtree: "
                f"{StructureSpecification.format_path(mount.path)}"
            )

        for element in mount.fragment.elements:
            if element.path == ():
                continue
            expanded_elements.append(
                StructureElement(
                    path=mount.path + element.path,
                    kind=element.kind,
                    required=element.required,
                )
            )
        for logical in mount.fragment.logical_elements:
            expanded_logical.append(
                LogicalStructureElement(
                    parent=mount.path + logical.parent,
                    logical_name=logical.logical_name,
                    fragment=logical.fragment,
                    names=logical.names,
                    min_count=logical.min_count,
                    max_count=logical.max_count,
                )
            )
        for group in mount.fragment.groups:
            expanded_groups.append(
                StructureGroup(
                    parent=mount.path + group.parent,
                    members=group.members,
                    min_count=group.min_count,
                    max_count=group.max_count,
                )
            )
        for recursive in mount.fragment._recursive_elements:
            expanded_recursive.append(
                _RecursiveStructureElement(
                    parent=mount.path + recursive.parent,
                    logical_name=recursive.logical_name,
                    names=recursive.names,
                    max_count=recursive.max_count,
                    template=(
                        mount.fragment
                        if recursive.template is None
                        else recursive.template
                    ),
                )
            )
        for path in mount.fragment._unconstrained_paths:
            unconstrained_paths.append(mount.path + path)

    by_path: dict[tuple[str, ...], StructureElement] = {}
    for element in expanded_elements:
        if element.path in by_path:
            raise ValueError(
                f"duplicate {owner} path: "
                f"{StructureSpecification.format_path(element.path)}"
            )
        by_path[element.path] = element

    if () not in by_path:
        raise ValueError(f"{owner} must contain a root element")
    if not by_path[()].required:
        raise ValueError(f"{owner} root element must be required")

    for path in by_path:
        if path and path[:-1] not in by_path:
            raise ValueError(
                f"{owner} path has no parent: "
                f"{StructureSpecification.format_path(path)}"
            )

    unique_unconstrained: list[tuple[str, ...]] = []
    for path in unconstrained_paths:
        if path not in by_path:
            raise ValueError(
                "unconstrained subtree root is not defined: "
                f"{StructureSpecification.format_path(path)}"
            )
        if path not in unique_unconstrained:
            unique_unconstrained.append(path)

    for path in unique_unconstrained:
        if any(other != path and other[: len(path)] == path for other in by_path):
            raise ValueError(
                "an unconstrained subtree cannot contain concrete child rules: "
                f"{StructureSpecification.format_path(path)}"
            )

    for logical in expanded_logical:
        if logical.parent not in by_path:
            raise ValueError(
                "logical structure element parent is not defined: "
                f"{StructureSpecification.format_path(logical.parent)}"
            )
        if any(logical.parent[: len(path)] == path for path in unique_unconstrained):
            raise ValueError(
                "an unconstrained subtree cannot contain logical child rules: "
                f"{StructureSpecification.format_path(logical.parent)}"
            )
        if logical.names is not None:
            explicit_names = {
                path[-1] for path in by_path if path and path[:-1] == logical.parent
            }
            eligible_names = set(logical.names) - explicit_names
            if logical.min_count > len(eligible_names):
                raise ValueError(
                    "logical structure element min_count cannot be satisfied after "
                    "explicit-element precedence at "
                    f"{StructureSpecification.format_path(logical.parent)}"
                )

    for recursive in expanded_recursive:
        if recursive.parent not in by_path:
            raise ValueError(
                "recursive structure parent is not defined: "
                f"{StructureSpecification.format_path(recursive.parent)}"
            )
        if any(recursive.parent[: len(path)] == path for path in unique_unconstrained):
            raise ValueError(
                "an unconstrained subtree cannot contain recursive child rules: "
                f"{StructureSpecification.format_path(recursive.parent)}"
            )

    normalized_groups: list[StructureGroup] = []
    for group in expanded_groups:
        if group.parent not in by_path:
            raise ValueError(
                "structure group parent is not defined: "
                f"{StructureSpecification.format_path(group.parent)}"
            )
        if any(group.parent[: len(path)] == path for path in unique_unconstrained):
            raise ValueError(
                "an unconstrained subtree cannot contain structure groups: "
                f"{StructureSpecification.format_path(group.parent)}"
            )
        member_elements: list[StructureElement] = []
        for name in group.members:
            member = by_path.get(group.parent + (name,))
            if member is None:
                raise ValueError(
                    "structure group members must name exact children of their parent: "
                    f"{StructureSpecification.format_path(group.parent + (name,))}"
                )
            member_elements.append(member)
        required_count = sum(member.required for member in member_elements)
        if group.max_count is not None and required_count > group.max_count:
            raise ValueError(
                "structure group max_count cannot be lower than its number of "
                "required members"
            )
        normalized_groups.append(group)

    _validate_logical_rule_uniqueness(
        tuple(expanded_elements),
        tuple(expanded_logical),
        tuple(expanded_recursive),
    )

    return (
        tuple(expanded_elements),
        tuple(expanded_logical),
        tuple(normalized_groups),
        tuple(unique_unconstrained),
        tuple(expanded_recursive),
    )


class Structure(ABC):
    """Interprets the placement and containment of runtime subjects."""

    @abstractmethod
    def resolve(self, focus: Focus) -> ResolvedStructure:
        """Resolve semantic structure centered on *focus*."""


class PythonStructure(Structure):
    """Minimal structure for Python packages, modules, and classes.

    A module focus contains classes defined by that module, including nested
    classes defined lexically inside those classes. Imported classes and class
    aliases are not treated as local entities. A package is classified as a
    package module but child modules are not imported implicitly; runtime
    discovery remains explicit at this stage of the implementation.
    """

    def resolve(self, focus: Focus) -> ResolvedStructure:
        subject = focus.subject

        if isinstance(subject, ModuleType):
            return self._resolve_module(focus, subject)
        if isinstance(subject, type):
            return self._resolve_entity(focus, subject)

        raise UnsupportedFocusError(
            f"PythonStructure cannot interpret focus of type {type(subject).__name__}"
        )

    def _resolve_module(self, focus: Focus, module: ModuleType) -> ResolvedStructure:
        module_path = (
            focus.placement
            if focus.placement is not None
            else tuple(module.__name__.split("."))
        )
        module_kind = (
            StructuralKind.PACKAGE
            if hasattr(module, "__path__")
            else StructuralKind.MODULE
        )
        nodes: list[StructureNode] = [
            StructureNode(
                subject=module,
                kind=module_kind,
                name=module.__name__.rsplit(".", 1)[-1],
                path=module_path,
            )
        ]

        for entity, parent in self._local_entities(module):
            nodes.append(
                StructureNode(
                    subject=entity,
                    kind=StructuralKind.ENTITY,
                    name=entity.__name__,
                    path=module_path + tuple(entity.__qualname__.split(".")),
                    parent=parent,
                )
            )

        return ResolvedStructure(focus=focus, nodes=tuple(nodes))

    def _resolve_entity(self, focus: Focus, entity: type[object]) -> ResolvedStructure:
        entity_path = (
            focus.placement
            if focus.placement is not None
            else tuple(entity.__module__.split("."))
            + tuple(entity.__qualname__.split("."))
        )
        node = StructureNode(
            subject=entity,
            kind=StructuralKind.ENTITY,
            name=entity.__name__,
            path=entity_path,
        )
        return ResolvedStructure(focus=focus, nodes=(node,))

    @staticmethod
    def _local_entities(
        module: ModuleType,
    ) -> Iterable[tuple[type[object], object]]:
        seen: set[int] = set()
        candidates = cast(Iterable[object], vars(module).values())
        for candidate in candidates:
            if not isinstance(candidate, type):
                continue
            if candidate.__module__ != module.__name__:
                continue
            if "." in candidate.__qualname__ or "<locals>" in candidate.__qualname__:
                continue
            yield from PythonStructure._entity_tree(
                candidate,
                module=module,
                parent=module,
                seen=seen,
            )

    @staticmethod
    def _entity_tree(
        entity: type[object],
        *,
        module: ModuleType,
        parent: object,
        seen: set[int],
    ) -> Iterator[tuple[type[object], object]]:
        identity = id(entity)
        if identity in seen:
            return
        seen.add(identity)
        yield entity, parent

        prefix = entity.__qualname__ + "."
        candidates = cast(Iterable[object], vars(entity).values())
        for candidate in candidates:
            if not isinstance(candidate, type):
                continue
            if candidate.__module__ != module.__name__:
                continue
            if not candidate.__qualname__.startswith(prefix):
                continue
            relative = candidate.__qualname__[len(prefix) :]
            if "." in relative or "<locals>" in relative:
                continue
            yield from PythonStructure._entity_tree(
                candidate,
                module=module,
                parent=entity,
                seen=seen,
            )
