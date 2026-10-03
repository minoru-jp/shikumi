from __future__ import annotations

import shikumi
from shikumi import standard


def test_core_public_surface_matches_api_reference_layering() -> None:
    expected = {
        "Cardinality",
        "ClassBinding",
        "Diagnostic",
        "DiagnosticSeverity",
        "DescriptorUse",
        "DescriptorUseRule",
        "Focus",
        "Information",
        "InformationType",
        "LogicalStructureElement",
        "PythonStructure",
        "RealizationCheck",
        "Realizer",
        "ResolvedStructure",
        "SemanticView",
        "Shikumi",
        "ShikumiError",
        "StructuralKind",
        "Structure",
        "StructureBinding",
        "StructureCheck",
        "StructureElement",
        "StructureFragment",
        "StructureGroup",
        "StructureMount",
        "StructureNode",
        "StructureSelector",
        "StructureSpecification",
        "UnknownViewSubjectError",
        "UnsupportedFocusError",
        "ValidationResult",
        "ValidationRule",
        "ViewItem",
        "attach_information",
        "check_descriptor_uses",
        "check_structure",
        "class_binding",
        "clear_descriptor_uses",
        "clear_information",
        "descriptor_uses_of",
        "information_of",
        "record_descriptor_use",
        "validator",
    }

    assert set(shikumi.__all__) == expected
    assert not hasattr(shikumi, "assignment")
    assert not hasattr(shikumi, "decorator")


def test_standard_public_surface_matches_api_reference_layering() -> None:
    expected = {
        "DocstringWriter",
        "PackageTreeStructure",
        "assignment",
        "content_type",
        "decorator",
        "docstring",
        "information_type_rule",
    }

    assert set(standard.__all__) == expected
