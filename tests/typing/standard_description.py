"""Consumer-side static typing contract for the standard description writers."""

from __future__ import annotations

from typing import assert_type

from shikumi import InformationType
from shikumi.standard import assignment, decorator


Title = InformationType("title", str)

title = assignment(Title)
assert_type(title.information_type, InformationType[str])


class Page:
    title @= "Overview"
    title @= "Details"


# These ignores are intentionally part of the contract. Under ``--strict``,
# mypy's unused-ignore check makes this file fail if the writer ever stops
# rejecting values outside the InformationType's type parameter.
title.__imatmul__(123)  # type: ignore


class InvalidPage:
    title @= 123  # type: ignore


title_decorator = decorator(Title)
assert_type(title_decorator.information_type, InformationType[str])


@title_decorator("Overview")
class DecoratedPage:
    pass


title_decorator(123)  # type: ignore
