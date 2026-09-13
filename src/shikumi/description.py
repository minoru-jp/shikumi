"""Runtime facts about description-writer use and their structural rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final

from ._weak_identity import WeakIdentityRegistry
from .structure import StructuralKind


@dataclass(frozen=True, slots=True)
class DescriptorUse:
    """One runtime fact that a description writer was used on a subject.

    This records *how description was performed*, independently of any
    information records that the writer may have attached. One descriptor use
    may produce zero, one, or many information attachments.
    """

    descriptor: object
    subject: object


@dataclass(frozen=True, slots=True)
class _DescriptorUseRecord:
    """Registry representation that deliberately does not retain the subject."""

    descriptor: object


_DESCRIPTOR_USES: Final[WeakIdentityRegistry[_DescriptorUseRecord]] = (
    WeakIdentityRegistry(
        subject_error="descriptor-use subjects must support weak references"
    )
)


def record_descriptor_use(subject: object, descriptor: object) -> DescriptorUse:
    """Record that *descriptor* was used on runtime *subject*.

    The descriptor is kept as a Python object rather than converted to a name.
    Bound methods are matched by their bound instance and underlying function,
    so repeated attribute access such as ``writer.describe`` remains stable.
    """

    _DESCRIPTOR_USES.append(
        subject,
        _DescriptorUseRecord(descriptor=descriptor),
    )
    return DescriptorUse(descriptor=descriptor, subject=subject)


def descriptor_uses_of(subject: object) -> tuple[DescriptorUse, ...]:
    """Return descriptor uses directly recorded for *subject* in use order."""

    return tuple(
        DescriptorUse(descriptor=record.descriptor, subject=subject)
        for record in _DESCRIPTOR_USES.get(subject)
    )


def clear_descriptor_uses(subject: object) -> None:
    """Remove descriptor-use facts directly recorded for *subject*."""

    _DESCRIPTOR_USES.clear(subject)


def same_descriptor(left: object, right: object) -> bool:
    """Return whether two runtime values identify the same descriptor surface.

    Ordinary objects use identity. Bound Python methods additionally compare
    by bound instance and underlying function, because each attribute access
    creates a fresh bound-method object.
    """

    if left is right:
        return True

    left_self = getattr(left, "__self__", None)
    right_self = getattr(right, "__self__", None)
    left_func = getattr(left, "__func__", None)
    right_func = getattr(right, "__func__", None)
    return (
        left_self is not None
        and right_self is not None
        and left_self is right_self
        and left_func is not None
        and right_func is not None
        and left_func is right_func
    )


def _normalize_path(
    value: tuple[str, ...] | None,
    *,
    field: str,
) -> tuple[str, ...] | None:
    if value is None:
        return None
    if isinstance(value, str):
        raise TypeError(f"{field} must be a tuple of path components")
    normalized = tuple(value)
    if any(not isinstance(part, str) or not part for part in normalized):
        raise ValueError(f"{field} components must be non-empty strings")
    return normalized


@dataclass(frozen=True, slots=True, kw_only=True)
class StructureSelector:
    """Select structural positions where a descriptor may be used.

    ``kind`` restricts the structural kind. ``at`` selects one exact effective
    root-relative path. ``under`` selects a path and all of its descendants,
    including the path itself. ``at`` and ``under`` are mutually exclusive.
    With no fields set, the selector matches every structural position.
    """

    kind: StructuralKind | None = None
    at: tuple[str, ...] | None = None
    under: tuple[str, ...] | None = None
    _alternatives: tuple["StructureSelector", ...] = field(
        default=(),
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        if self.kind is not None and not isinstance(self.kind, StructuralKind):
            raise TypeError("structure selector kind must be a StructuralKind")
        normalized_at = _normalize_path(self.at, field="structure selector at")
        normalized_under = _normalize_path(
            self.under,
            field="structure selector under",
        )
        if normalized_at is not None and normalized_under is not None:
            raise ValueError("structure selector cannot specify both at and under")
        object.__setattr__(self, "at", normalized_at)
        object.__setattr__(self, "under", normalized_under)

    @classmethod
    def one_of(cls, *selectors: "StructureSelector") -> "StructureSelector":
        """Return a selector matching any of *selectors*."""

        if not selectors:
            raise ValueError("StructureSelector.one_of requires at least one selector")
        if any(not isinstance(selector, StructureSelector) for selector in selectors):
            raise TypeError("StructureSelector.one_of accepts only StructureSelector objects")
        combined = cls()
        flattened: list[StructureSelector] = []
        for selector in selectors:
            if selector._alternatives:
                flattened.extend(selector._alternatives)
            else:
                flattened.append(selector)
        object.__setattr__(combined, "_alternatives", tuple(flattened))
        return combined

    def __or__(self, other: "StructureSelector") -> "StructureSelector":
        if not isinstance(other, StructureSelector):
            return NotImplemented
        return self.one_of(self, other)

    def matches(self, *, kind: StructuralKind, path: tuple[str, ...]) -> bool:
        """Return whether one effective structural position is selected."""

        if self._alternatives:
            return any(
                selector.matches(kind=kind, path=path)
                for selector in self._alternatives
            )
        if self.kind is not None and kind is not self.kind:
            return False
        if self.at is not None and path != self.at:
            return False
        if self.under is not None and path[: len(self.under)] != self.under:
            return False
        return True


@dataclass(frozen=True, slots=True, eq=False)
class DescriptorUseRule:
    """Regulate where one description writer may and should be used.

    A use outside ``allowed`` is an error. A use inside ``allowed`` but outside
    ``recommended`` is a warning. If ``recommended`` is omitted, every allowed
    position is considered equally recommended.
    """

    descriptor: object
    allowed: StructureSelector
    recommended: StructureSelector | None = None
    name: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.allowed, StructureSelector):
            raise TypeError("descriptor-use rule allowed must be a StructureSelector")
        if self.recommended is not None and not isinstance(
            self.recommended,
            StructureSelector,
        ):
            raise TypeError(
                "descriptor-use rule recommended must be a StructureSelector or None"
            )
        if self.name == "":
            raise ValueError("descriptor-use rule name must not be empty")

    @property
    def display_name(self) -> str:
        if self.name is not None:
            return self.name

        function = getattr(self.descriptor, "__func__", None)
        bound_to = getattr(self.descriptor, "__self__", None)
        if function is not None and bound_to is not None:
            owner = type(bound_to).__name__
            return f"{owner}.{getattr(function, '__name__', type(function).__name__)}"

        qualname = getattr(self.descriptor, "__qualname__", None)
        if isinstance(qualname, str):
            return qualname
        name = getattr(self.descriptor, "__name__", None)
        if isinstance(name, str):
            return name
        return type(self.descriptor).__name__
