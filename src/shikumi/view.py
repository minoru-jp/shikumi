"""Semantic view produced by interpreting a focus through a Shikumi."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator, TypeVar, cast

from .description import DescriptorUse, same_descriptor
from .errors import UnknownViewSubjectError
from .information import Information, InformationType
from .structure import Focus, ResolvedStructure, StructuralKind, StructureNode


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ViewItem:
    """One interpreted subject in a semantic view."""

    node: StructureNode
    information: tuple[Information[Any], ...]
    descriptor_uses: tuple[DescriptorUse, ...] = ()

    @property
    def subject(self) -> object:
        return self.node.subject

    @property
    def kind(self) -> StructuralKind:
        return self.node.kind

    def records(
        self,
        information_type: InformationType[T],
    ) -> tuple[Information[T], ...]:
        """Return records of *information_type* by identity."""

        records = tuple(
            record
            for record in self.information
            if record.type is information_type
        )
        return cast(tuple[Information[T], ...], records)

    def values(self, information_type: InformationType[T]) -> tuple[T, ...]:
        """Return values of *information_type* by identity."""

        return tuple(record.value for record in self.records(information_type))

    def has(self, information_type: InformationType[T]) -> bool:
        """Return whether this item has at least one matching record."""

        return any(record.type is information_type for record in self.information)

    def uses(self, descriptor: object) -> tuple[DescriptorUse, ...]:
        """Return uses of *descriptor* recorded for this subject."""

        return tuple(
            use
            for use in self.descriptor_uses
            if same_descriptor(use.descriptor, descriptor)
        )


@dataclass(frozen=True, slots=True)
class SemanticView:
    """Meaning observed by a Shikumi around one focus."""

    focus: Focus
    structure: ResolvedStructure
    items: tuple[ViewItem, ...]

    def __post_init__(self) -> None:
        if len(self.structure.nodes) != len(self.items):
            raise ValueError("semantic view items must correspond to structure nodes")
        for node, item in zip(self.structure.nodes, self.items, strict=True):
            if item.node is not node:
                raise ValueError("semantic view item order must match structure nodes")

    @property
    def focused(self) -> ViewItem:
        """Return the item corresponding to the view focus."""

        return self.item(self.focus.subject)

    @property
    def entities(self) -> tuple[ViewItem, ...]:
        return tuple(item for item in self.items if item.kind is StructuralKind.ENTITY)

    @property
    def modules(self) -> tuple[ViewItem, ...]:
        return tuple(item for item in self.items if item.kind is StructuralKind.MODULE)

    @property
    def packages(self) -> tuple[ViewItem, ...]:
        return tuple(item for item in self.items if item.kind is StructuralKind.PACKAGE)

    def item(self, subject: object) -> ViewItem:
        """Return the view item whose subject is *subject* by identity."""

        for item in self.items:
            if item.subject is subject:
                return item
        raise UnknownViewSubjectError("subject is not present in this semantic view")

    def subview(self, subject: object) -> SemanticView:
        """Return the already-interpreted subtree focused on *subject*.

        The returned view reuses this view's resolved nodes, information, and
        descriptor-use records. It does not ask the owning :class:`Shikumi` to
        interpret Python runtime state again.
        """

        focused = self.item(subject)
        if focused.subject is self.focus.subject:
            return self

        root_path = focused.node.path
        selected_items = tuple(
            item
            for item in self.items
            if item.node.path[: len(root_path)] == root_path
        )
        selected_nodes = tuple(item.node for item in selected_items)
        focus = Focus(focused.subject, placement=root_path)
        structure = ResolvedStructure(focus=focus, nodes=selected_nodes)
        return SemanticView(focus=focus, structure=structure, items=selected_items)

    def __iter__(self) -> Iterator[ViewItem]:
        return iter(self.items)
