"""Public surface for the Shikumi core."""

from .binding import class_binding
from .description import (
    DescriptorUse,
    DescriptorUseRule,
    StructureSelector,
    clear_descriptor_uses,
    descriptor_uses_of,
    record_descriptor_use,
)
from .errors import ShikumiError, UnknownViewSubjectError, UnsupportedFocusError
from .information import (
    Cardinality,
    Information,
    InformationType,
    attach_information,
    clear_information,
    information_of,
)
from .model import Shikumi
from .realization import RealizationCheck, Realizer
from .structure import (
    Focus,
    LogicalStructureElement,
    PythonStructure,
    ResolvedStructure,
    StructuralKind,
    Structure,
    StructureElement,
    StructureFragment,
    StructureGroup,
    StructureMount,
    StructureNode,
    StructureSpecification,
)
from .validation import (
    Diagnostic,
    DiagnosticSeverity,
    StructureBinding,
    StructureCheck,
    ValidationResult,
    ValidationRule,
    check_descriptor_uses,
    check_structure,
    validator,
)
from .view import SemanticView, ViewItem

__all__ = [
    "Cardinality",
    "Diagnostic",
    "DiagnosticSeverity",
    "DescriptorUse",
    "DescriptorUseRule",
    "Focus",
    "LogicalStructureElement",
    "Information",
    "InformationType",
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
]
