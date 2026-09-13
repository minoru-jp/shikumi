from __future__ import annotations

from shikumi import InformationType, Shikumi, attach_information, clear_information
from shikumi.standard import information_type_rule


def test_standard_information_rule_checks_cardinality() -> None:
    Title = InformationType("title", str)

    class Page:
        pass

    try:
        attach_information(Page, Title, "One")
        attach_information(Page, Title, "Two")
        result = Shikumi(
            information_types=[Title],
            validators=[information_type_rule(Title)],
        ).validate(Page)

        assert not result.is_valid
        assert [item.code for item in result.diagnostics] == [
            "information.cardinality"
        ]
    finally:
        clear_information(Page)


def test_standard_information_rule_checks_value_type_at_validation_time() -> None:
    Title = InformationType("title", str)

    class Page:
        pass

    try:
        attach_information(Page, Title, 10)
        result = Shikumi(
            information_types=[Title],
            validators=[information_type_rule(Title)],
        ).validate(Page)

        assert not result.is_valid
        assert [item.code for item in result.diagnostics] == [
            "information.value_type"
        ]
    finally:
        clear_information(Page)
