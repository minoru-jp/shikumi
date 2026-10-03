"""Low-level runtime binding helpers for class-body descriptions."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class _ClassBinding(Generic[T]):
    """Temporary class-body value that applies callbacks after class creation."""

    values: tuple[T, ...]
    connect: Callable[[type[object], T], None]

    def __imatmul__(self, value: T) -> _ClassBinding[T]:
        """Accumulate another value written to the same class-body name."""

        return _ClassBinding(self.values + (value,), self.connect)

    def __set_name__(self, owner: type[object], name: str) -> None:
        for value in self.values:
            self.connect(owner, value)

        # The binding is class-creation scaffolding, not a semantic attribute.
        # Remove it only when the class still holds this exact temporary value.
        if owner.__dict__.get(name) is self:
            delattr(owner, name)


def class_binding(
    value: T,
    connect: Callable[[type[object], T], None],
) -> object:
    """Apply *connect* to a class after the class body has finished executing.

    The helper intentionally assigns no meaning to *value*.  It only preserves
    the value until the class object exists and then calls ``connect(subject,
    value)``.  The returned temporary object also accepts repeated ``@=`` writes
    to the same class-body name and replays them in order.
    """

    if not callable(connect):
        raise TypeError("connect must be callable")  # pyright: ignore[reportUnreachable]
    return _ClassBinding((value,), connect)
