"""Consumer-side static typing contract for custom ``@=`` writers."""

from __future__ import annotations

from typing import assert_type

from shikumi import ClassBinding, class_binding


def _connect(subject: type[object], value: str) -> None:
    del subject, value


binding = class_binding("first", _connect)
assert_type(binding, ClassBinding[str])
binding @= "second"

# The binding preserves the value type across repeated writes.
binding.__imatmul__(123)  # pyright: ignore[reportArgumentType]


class Tags:
    def __imatmul__(self, value: str):
        return class_binding(value, self._connect)

    @staticmethod
    def _connect(subject: type[object], value: str) -> None:
        del subject, value


tags = Tags()


class Page:
    tags @= "python"
    tags @= "runtime"


class InvalidPage:
    tags @= 123  # pyright: ignore[reportOperatorIssue]
