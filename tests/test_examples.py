from __future__ import annotations

from structure_showcase.invalid import (
    bad_named,
    closed_ordinary,
    empty_collection,
    group_both,
    missing_required,
)
from structure_showcase.specification import showcase, showcase_structure
from structure_showcase.valid import combined, minimal


def _validate(package):
    return showcase.validate(
        package,
        placement=(),
        structure_specification=showcase_structure,
    )


def test_structure_showcase_accepts_minimal_and_combined_fixtures() -> None:
    for package in (minimal, combined):
        result = _validate(package)
        assert result.is_valid, (package.__name__, result.diagnostics)


def test_structure_showcase_combined_fixture_exercises_logical_bindings() -> None:
    result = _validate(combined)
    assert result.structure_check is not None

    bindings = {
        (binding.logical_element.logical_name, binding.actual_path)
        for binding in result.structure_check.bindings
    }
    assert ("entry", ("collection", "alpha")) in bindings
    assert ("variant", ("named", "alpha")) in bindings
    assert ("package_child", ("mixed", "package_child")) in bindings
    assert ("module_child", ("mixed", "module_child")) in bindings
    assert ("branch", ("tree", "branch")) in bindings
    assert ("branch", ("tree", "branch", "nested")) in bindings
    assert ("module_leaf", ("tree", "branch", "nested", "leaf")) in bindings
    assert ("ordinary", ("override", "ordinary")) in bindings
    assert not any(path == ("override", "special") for _, path in bindings)


def test_structure_showcase_invalid_fixtures_have_stable_diagnostics() -> None:
    cases = (
        (missing_required, {"structure.element.missing"}),
        (empty_collection, {"structure.logical.minimum"}),
        (bad_named, {"structure.logical.minimum", "structure.element.unexpected"}),
        (group_both, {"structure.group.maximum"}),
        (closed_ordinary, {"structure.element.unexpected"}),
    )

    for package, expected_codes in cases:
        result = _validate(package)
        assert not result.is_valid, package.__name__
        assert {diagnostic.code for diagnostic in result.diagnostics} == expected_codes
