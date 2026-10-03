"""Reusable description writers built only from Shikumi Core primitives."""

from __future__ import annotations

from collections.abc import Callable
from inspect import cleandoc
from typing import Any, Generic, Self, TypeVar, cast

from ..binding import class_binding
from ..description import record_descriptor_use
from ..information import InformationType, attach_information

T = TypeVar("T")
S = TypeVar("S")


class _AssignmentWriter(Generic[T]):
    """Standard ``@=`` writer that attaches values without interpretation."""

    __slots__: tuple[str, ...] = ("information_type",)
    information_type: InformationType[T]

    def __init__(self, information_type: InformationType[T]) -> None:
        self.information_type = information_type

    def __imatmul__(self, value: T) -> Self:
        # At runtime ``@=`` replaces the class-body name with a temporary
        # _ClassBinding.  Statically, however, the name must remain the same
        # writer type so repeated ``@=`` operations keep checking ``T``.
        return cast(Self, class_binding(value, self._connect))

    def _connect(self, subject: type[object], value: T) -> None:
        _ = record_descriptor_use(subject, self)
        _ = attach_information(
            subject,
            self.information_type,
            value,
        )


class _DecoratorWriter(Generic[T]):
    """Standard decorator writer that attaches values without interpretation."""

    __slots__: tuple[str, ...] = ("information_type",)
    information_type: InformationType[T]

    def __init__(self, information_type: InformationType[T]) -> None:
        self.information_type = information_type

    def __call__(self, value: T) -> Callable[[S], S]:
        def apply(subject: S) -> S:
            _ = record_descriptor_use(subject, self)
            _ = attach_information(
                subject,
                self.information_type,
                value,
            )
            return subject

        return apply


class DocstringWriter:
    """Write string information from an explicitly decorated object's docstring."""

    __slots__: tuple[str, ...] = ("clean", "information_type", "required")
    information_type: InformationType[Any]
    clean: bool
    required: bool

    def __init__(
        self,
        information_type: InformationType[Any],
        *,
        clean: bool = True,
        required: bool = False,
    ) -> None:
        if not information_type.accepts(""):
            raise TypeError(
                "docstring writers require an information type accepting str"
            )
        self.information_type = information_type
        self.clean = clean
        self.required = required

    def __call__(self, subject: S) -> S:
        _ = record_descriptor_use(subject, self)
        raw = getattr(subject, "__doc__", None)
        if raw is None:
            if self.required:
                raise ValueError("docstring writer requires a docstring")
            return subject
        if not isinstance(raw, str):
            raise TypeError("subject __doc__ must be a string or None")

        value = cleandoc(raw) if self.clean else raw
        _ = attach_information(
            subject,
            self.information_type,
            value,
        )
        return subject


def assignment(information_type: InformationType[T]) -> _AssignmentWriter[T]:
    """Create a standard ``@=`` writer for *information_type*."""

    return _AssignmentWriter(information_type)


def decorator(information_type: InformationType[T]) -> _DecoratorWriter[T]:
    """Create a standard value-taking decorator writer for *information_type*."""

    return _DecoratorWriter(information_type)


def docstring(
    information_type: InformationType[Any],
    *,
    clean: bool = True,
    required: bool = False,
) -> DocstringWriter:
    """Create a standard docstring description writer."""

    return DocstringWriter(
        information_type,
        clean=clean,
        required=required,
    )
