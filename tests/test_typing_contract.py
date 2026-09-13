from __future__ import annotations

from typing import get_args, get_type_hints

from shikumi import Information, InformationType, ViewItem, attach_information


def test_information_type_and_information_are_generic() -> None:
    assert len(InformationType.__parameters__) == 1
    assert len(Information.__parameters__) == 1

    init_hints = get_type_hints(InformationType.__init__)
    value_type_options = get_args(init_hints["value_type"])
    constructor_type_variable = get_args(value_type_options[0])[0]

    assert constructor_type_variable is InformationType.__parameters__[0]


def test_attach_information_preserves_information_value_type_variable() -> None:
    hints = get_type_hints(attach_information)

    information_type_argument = get_args(hints["information_type"])[0]
    return_argument = get_args(hints["return"])[0]

    assert hints["value"] is information_type_argument
    assert return_argument is information_type_argument


def test_view_item_records_and_values_preserve_information_type_variable() -> None:
    records_hints = get_type_hints(ViewItem.records)
    values_hints = get_type_hints(ViewItem.values)

    records_type_variable = get_args(records_hints["information_type"])[0]
    records_return_information = get_args(records_hints["return"])[0]
    records_return_type_variable = get_args(records_return_information)[0]

    values_type_variable = get_args(values_hints["information_type"])[0]
    values_return_type_variable = get_args(values_hints["return"])[0]

    assert records_return_type_variable is records_type_variable
    assert values_return_type_variable is values_type_variable


def test_internal_strict_typing_signatures_are_annotated() -> None:
    import inspect

    from shikumi._weak_identity import WeakIdentityRegistry
    from shikumi.standard.validation import information_type_rule

    cleanup = inspect.signature(WeakIdentityRegistry._cleanup_callback)
    assert cleanup.return_annotation is not inspect.Signature.empty

    factory = inspect.signature(information_type_rule)
    assert factory.return_annotation is not inspect.Signature.empty


def test_standard_writer_factories_preserve_information_value_type_variable() -> None:
    from shikumi.standard.description import assignment, decorator

    assignment_hints = get_type_hints(assignment)
    assignment_argument = get_args(assignment_hints["information_type"])[0]
    assignment_return = get_args(assignment_hints["return"])[0]

    decorator_hints = get_type_hints(decorator)
    decorator_argument = get_args(decorator_hints["information_type"])[0]
    decorator_return = get_args(decorator_hints["return"])[0]

    assert assignment_return is assignment_argument
    assert decorator_return is decorator_argument
