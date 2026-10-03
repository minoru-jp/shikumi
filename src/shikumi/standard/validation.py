"""Reusable validation-rule constructors for standard information semantics."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, cast

from ..information import Cardinality, InformationType
from ..structure import StructuralKind
from ..validation import Diagnostic, ValidationRule, validator
from ..view import SemanticView


def information_type_rule(
    information_type: InformationType[Any],
    *,
    focus: StructuralKind = StructuralKind.ENTITY,
) -> ValidationRule:
    """Validate Python value type and cardinality for one information type."""

    @validator(
        focus=focus,
        name=f"{information_type.name}.information_type",
    )
    def validate_information(view: SemanticView) -> Iterator[Diagnostic]:
        records = view.focused.records(information_type)

        if information_type.cardinality is Cardinality.ONE and len(records) > 1:
            yield Diagnostic(
                f"information {information_type.name!r} allows one value, "
                f"but {len(records)} values are present",
                code="information.cardinality",
            )

        for record in records:
            value = cast(object, record.value)
            if not information_type.accepts(value):
                yield Diagnostic(
                    f"information {information_type.name!r} does not accept value "
                    f"of type {type(value).__name__}",
                    code="information.value_type",
                )

    return validate_information
