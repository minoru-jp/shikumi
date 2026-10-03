"""Low-level runtime binding helpers for class-body descriptions."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, Protocol, Self, TypeVar

T = TypeVar("T")
T_contra = TypeVar("T_contra", contravariant=True)


class ClassBinding(Protocol[T_contra]):
    """Static contract for the temporary value returned by :func:`class_binding`.

    A class binding accepts additional ``@=`` writes with the same value type.
    Its concrete runtime representation is intentionally not part of the public
    contract.
    """

    def __imatmul__(self, value: T_contra) -> Self:
        """Accumulate another value written to the same class-body name."""
        ...


@dataclass(frozen=True, slots=True)
class _ClassBinding(Generic[T]):
    """Temporary class-body value that connects during class creation.

    The current implementation replays the callback from ``__set_name__``
    after the class body has finished executing and before
    ``__init_subclass__`` runs.
    """

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
) -> ClassBinding[T]:
    """Apply *connect* after the class body and before ``__init_subclass__``.

    The helper intentionally assigns no meaning to *value*.  The current
    implementation preserves values until ``__set_name__`` runs during class
    creation and then calls ``connect(subject, value)``.  Exceptions raised by
    *connect* are not normalized by Shikumi; their externally visible form
    follows the Python runtime's class-creation behavior.  On Python 3.11, an
    exception raised from ``__set_name__`` is wrapped in ``RuntimeError``; on
    Python 3.12 and later, the original exception is propagated with a runtime
    note.  The returned
    temporary object also accepts repeated ``@=`` writes to the same class-body
    name and replays them in order.
    """

    if not callable(connect):
        raise TypeError("connect must be callable")  # pyright: ignore[reportUnreachable]
    return _ClassBinding((value,), connect)
