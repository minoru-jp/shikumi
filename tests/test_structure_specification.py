from __future__ import annotations

import types

import pytest

from shikumi import (
    Focus,
    Shikumi,
    StructuralKind,
    StructureElement,
    StructureSpecification,
)


def _module(name: str, source: str) -> types.ModuleType:
    module = types.ModuleType(name)
    exec(compile(source, f"<{name}>", "exec"), module.__dict__)
    return module


def test_structure_specification_can_be_authored_explicitly() -> None:
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("api",), StructuralKind.PACKAGE),
            StructureElement(("api", "users"), StructuralKind.MODULE),
            StructureElement(("api", "users", "GetUser"), StructuralKind.ENTITY),
        ]
    )

    assert specification.element_at(("api", "users")).kind is StructuralKind.MODULE
    assert [element.path for element in specification.subtree(("api", "users"))] == [
        ("api", "users"),
        ("api", "users", "GetUser"),
    ]


def test_structure_specification_requires_a_complete_parent_chain() -> None:
    with pytest.raises(ValueError, match="no parent"):
        StructureSpecification(
            [
                StructureElement((), StructuralKind.PACKAGE),
                StructureElement(("api", "users"), StructuralKind.MODULE),
            ]
        )


def test_structure_specification_can_be_derived_from_a_description_body() -> None:
    reference = _module(
        "reference.users",
        """
class GetUser:
    class Response:
        pass
""",
    )

    specification = Shikumi().derive_structure_specification(reference)

    assert [(element.path, element.kind) for element in specification.elements] == [
        ((), StructuralKind.MODULE),
        (("GetUser",), StructuralKind.ENTITY),
        (("GetUser", "Response"), StructuralKind.ENTITY),
    ]


def test_standalone_module_validation_requires_explicit_placement() -> None:
    module = _module("scratch.users", "class GetUser: pass")

    with pytest.raises(ValueError, match="explicit placement"):
        Shikumi().validate(module)


def test_module_is_checked_against_the_specification_subtree_at_placement() -> None:
    module = _module("scratch.generated", "class GetUser: pass")
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("api",), StructuralKind.PACKAGE),
            StructureElement(("api", "users"), StructuralKind.MODULE),
            StructureElement(("api", "users", "GetUser"), StructuralKind.ENTITY),
            StructureElement(("api", "articles"), StructuralKind.MODULE),
        ]
    )

    result = Shikumi().validate(
        module,
        placement=("api", "users"),
        structure_specification=specification,
    )

    assert result.is_valid
    assert result.structure_check is not None
    assert result.structure_check.is_valid
    assert result.view.focused.node.path == ("api", "users")
    assert result.view.entities[0].node.path == ("api", "users", "GetUser")


def test_structure_check_reports_missing_and_unexpected_elements() -> None:
    module = _module("scratch.generated", "class Other: pass")
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.MODULE),
            StructureElement(("Expected",), StructuralKind.ENTITY),
        ]
    )

    result = Shikumi().validate(
        module,
        placement=(),
        structure_specification=specification,
    )

    assert not result.is_valid
    assert {diagnostic.code for diagnostic in result.diagnostics} == {
        "structure.element.missing",
        "structure.element.unexpected",
    }


def test_structure_check_rejects_an_undefined_placement() -> None:
    module = _module("scratch.generated", "class Item: pass")
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("known",), StructuralKind.MODULE),
        ]
    )

    result = Shikumi().validate(
        Focus(module, placement=("unknown",)),
        structure_specification=specification,
    )

    assert not result.is_valid
    assert result.diagnostics[0].code == "structure.placement.undefined"
