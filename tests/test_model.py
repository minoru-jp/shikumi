from __future__ import annotations

import pytest

from shikumi import Shikumi, Structure


class CustomStructure(Structure):
    def resolve(self, focus):
        raise AssertionError("constructor validation must not execute Structure.resolve()")


def test_shikumi_accepts_structure_subclasses_without_executing_them() -> None:
    structure = CustomStructure()

    shikumi = Shikumi(structure=structure)

    assert shikumi.structure is structure


def test_shikumi_rejects_non_structure_objects() -> None:
    with pytest.raises(TypeError, match="structure must be a Structure"):
        Shikumi(structure=object())  # type: ignore[arg-type]


def test_shikumi_rejects_non_information_type_entries() -> None:
    with pytest.raises(TypeError, match="information_types must contain InformationType"):
        Shikumi(information_types=[object()])  # type: ignore[list-item]


def test_shikumi_rejects_non_validation_rule_entries() -> None:
    with pytest.raises(TypeError, match="validators must contain ValidationRule"):
        Shikumi(validators=[object()])  # type: ignore[list-item]


def test_shikumi_rejects_non_descriptor_use_rule_entries() -> None:
    with pytest.raises(TypeError, match="descriptor_rules must contain DescriptorUseRule"):
        Shikumi(descriptor_rules=[object()])  # type: ignore[list-item]
