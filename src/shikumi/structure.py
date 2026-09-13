"""Structure concepts used to interpret Python runtime objects."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from types import ModuleType
from typing import Iterator

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
                raise ValueError("resolved structure contains duplicate subject identity")
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
    """One required kind at a root-relative structural path."""

    path: tuple[str, ...]
    kind: StructuralKind

    def __post_init__(self) -> None:
        if isinstance(self.path, str):
            raise TypeError("structure element path must be a tuple of path components")
        normalized = tuple(self.path)
        if any(not isinstance(part, str) or not part for part in normalized):
            raise ValueError("structure element path components must be non-empty strings")
        if not isinstance(self.kind, StructuralKind):
            raise TypeError("structure element kind must be a StructuralKind")
        object.__setattr__(self, "path", normalized)


@dataclass(frozen=True, slots=True, init=False)
class StructureSpecification:
    """A structural regulation expressed as exact root-relative elements.

    A specification can be authored explicitly by a regulation body or
    derived from an already resolved description body.  The representation is
    the same in both cases; callers choose the source explicitly.
    """

    elements: tuple[StructureElement, ...]

    def __init__(self, elements: Iterable[StructureElement]) -> None:
        normalized = tuple(elements)
        object.__setattr__(self, "elements", normalized)
        self._validate()

    def _validate(self) -> None:
        if not self.elements:
            raise ValueError("structure specification must contain at least one element")

        by_path: dict[tuple[str, ...], StructureElement] = {}
        for element in self.elements:
            if not isinstance(element, StructureElement):
                raise TypeError(
                    "structure specification elements must be StructureElement objects"
                )
            if element.path in by_path:
                raise ValueError(
                    f"duplicate structure specification path: {self.format_path(element.path)}"
                )
            by_path[element.path] = element

        if () not in by_path:
            raise ValueError("structure specification must contain a root element")

        for path in by_path:
            if path and path[:-1] not in by_path:
                raise ValueError(
                    "structure specification path has no parent: "
                    f"{self.format_path(path)}"
                )

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
                raise ValueError("resolved structure contains a node outside its focus root")
            relative = node.path[len(root_path) :]
            elements.append(StructureElement(path=relative, kind=node.kind))
        return cls(elements)

    def element_at(self, path: tuple[str, ...]) -> StructureElement | None:
        """Return the required element at *path*, if any."""

        normalized = tuple(path)
        for element in self.elements:
            if element.path == normalized:
                return element
        return None

    def subtree(self, placement: tuple[str, ...]) -> tuple[StructureElement, ...]:
        """Return elements at or below a root-relative placement."""

        normalized = tuple(placement)
        return tuple(
            element
            for element in self.elements
            if element.path[: len(normalized)] == normalized
        )

    @staticmethod
    def format_path(path: tuple[str, ...]) -> str:
        return ".".join(path) if path else "."


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
        for candidate in vars(module).values():
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
        for candidate in vars(entity).values():
            if not isinstance(candidate, type):
                continue
            if candidate.__module__ != module.__name__:
                continue
            if not candidate.__qualname__.startswith(prefix):
                continue
            relative = candidate.__qualname__[len(prefix):]
            if "." in relative or "<locals>" in relative:
                continue
            yield from PythonStructure._entity_tree(
                candidate,
                module=module,
                parent=entity,
                seen=seen,
            )
