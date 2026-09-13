"""Reusable standard information-type constructors."""

from __future__ import annotations

from typing import Any

from ..information import Cardinality, InformationType


def content_type(
    name: str = "content",
    *,
    value_type: type[Any] | tuple[type[Any], ...] = str,
) -> InformationType[Any]:
    """Create a single-valued information type for primary content."""

    return InformationType(
        name,
        value_type=value_type,
        cardinality=Cardinality.ONE,
    )
