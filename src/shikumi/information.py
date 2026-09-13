"""Runtime information model and low-level information attachment."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Final, Generic, Iterable, TypeVar, cast

from ._weak_identity import WeakIdentityRegistry


T = TypeVar("T")


class Cardinality(str, Enum):
    """How many values of an information type may conceptually occur."""

    ONE = "one"
    MANY = "many"


@dataclass(frozen=True, eq=False, slots=True)
class InformationType(Generic[T]):
    """Defines the semantic type of information understood by a Shikumi.

    Information types are identity-based. Two independently created types with
    the same name are still different semantic types.
    """

    name: str
    value_type: type[T] | tuple[type[Any], ...] = cast(type[T], object)
    cardinality: Cardinality = Cardinality.ONE

    def __post_init__(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("information type name must be a string")
        if not self.name:
            raise ValueError("information type name must not be empty")

        value_type = self.value_type
        candidates: tuple[object, ...]
        if isinstance(value_type, tuple):
            if not value_type:
                raise ValueError("information type value_type tuple must not be empty")
            candidates = value_type
        else:
            candidates = (value_type,)

        if any(not isinstance(item, type) for item in candidates):
            raise TypeError(
                "information type value_type must be a type or tuple of types"
            )
        for item in candidates:
            try:
                isinstance(None, item)
            except TypeError as exc:
                raise TypeError(
                    "information type value_type must be usable with isinstance"
                ) from exc

        if not isinstance(self.cardinality, Cardinality):
            raise TypeError("information type cardinality must be a Cardinality")

    def accepts(self, value: object) -> bool:
        """Return whether *value* matches this type's declared Python type."""

        return isinstance(value, self.value_type)


@dataclass(frozen=True, slots=True)
class Information(Generic[T]):
    """One runtime information record attached to a subject."""

    type: InformationType[T]
    value: T
    subject: object

    def __post_init__(self) -> None:
        if not isinstance(self.type, InformationType):
            raise TypeError("information type must be an InformationType")


@dataclass(frozen=True, slots=True)
class _InformationRecord:
    """Registry representation that deliberately does not retain the subject."""

    type: InformationType[Any]
    value: object


# Information is intentionally independent of Shikumi instances. Description
# mechanisms can attach information first; any compatible Shikumi may interpret
# it later. The registry is weak and identity-based, and its internal records do
# not retain the described subject.
_INFORMATION: Final[WeakIdentityRegistry[_InformationRecord]] = WeakIdentityRegistry(
    subject_error="information subjects must support weak references"
)


def attach_information(
    subject: object,
    information_type: InformationType[T],
    value: T,
) -> Information[T]:
    """Attach one semantic information record to a runtime *subject*.

    This is a low-level runtime primitive, not a description syntax. Future
    description mechanisms such as ``@=``, decorators, or docstrings build on
    this operation.
    """

    if not isinstance(information_type, InformationType):
        raise TypeError("information_type must be an InformationType")

    _INFORMATION.append(
        subject,
        _InformationRecord(type=information_type, value=value),
    )
    return Information(type=information_type, value=value, subject=subject)


def information_of(subject: object) -> tuple[Information[Any], ...]:
    """Return information directly attached to *subject* in attachment order."""

    return tuple(
        Information(type=record.type, value=record.value, subject=subject)
        for record in _INFORMATION.get(subject)
    )


def clear_information(subject: object) -> None:
    """Remove directly attached information from *subject*.

    Primarily useful for tests and tooling that manages runtime lifecycles.
    """

    _INFORMATION.clear(subject)


def select_information(
    subject: object,
    recognized_types: Iterable[InformationType[Any]],
) -> tuple[Information[Any], ...]:
    """Return records whose information type is recognized by identity."""

    recognized_ids = {id(item) for item in recognized_types}
    return tuple(
        record
        for record in information_of(subject)
        if id(record.type) in recognized_ids
    )
