"""Top-level Shikumi composition object."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from types import ModuleType
from typing import Any

from .description import DescriptorUseRule, descriptor_uses_of
from .information import InformationType, select_information
from .structure import Focus, PythonStructure, Structure, StructureSpecification
from .validation import (
    Diagnostic,
    ValidationResult,
    ValidationRule,
    check_descriptor_uses,
    check_structure,
)
from .view import SemanticView, ViewItem


@dataclass(frozen=True, slots=True, init=False)
class Shikumi:
    """Composes structure and recognized information into a semantic system."""

    structure: Structure
    information_types: tuple[InformationType[Any], ...]
    validators: tuple[ValidationRule, ...]
    descriptor_rules: tuple[DescriptorUseRule, ...]

    def __init__(
        self,
        *,
        structure: Structure | None = None,
        information_types: Iterable[InformationType[Any]] = (),
        validators: Iterable[ValidationRule] = (),
        descriptor_rules: Iterable[DescriptorUseRule] = (),
    ) -> None:
        resolved_structure = structure if structure is not None else PythonStructure()
        recognized = tuple(information_types)
        validation_rules = tuple(validators)
        descriptor_use_rules = tuple(descriptor_rules)
        self._validate_structure(resolved_structure)
        self._validate_information_types(recognized)
        self._validate_validators(validation_rules)
        self._validate_descriptor_rules(descriptor_use_rules)

        object.__setattr__(self, "structure", resolved_structure)
        object.__setattr__(self, "information_types", recognized)
        object.__setattr__(self, "validators", validation_rules)
        object.__setattr__(self, "descriptor_rules", descriptor_use_rules)

    @staticmethod
    def _validate_structure(structure: Structure) -> None:
        if not isinstance(structure, Structure):
            raise TypeError("structure must be a Structure")

    @staticmethod
    def _validate_information_types(
        information_types: tuple[InformationType[Any], ...],
    ) -> None:
        if any(not isinstance(item, InformationType) for item in information_types):
            raise TypeError("information_types must contain InformationType objects")
        identities = [id(item) for item in information_types]
        if len(identities) != len(set(identities)):
            raise ValueError("information_types must not contain the same object twice")

    @staticmethod
    def _validate_validators(
        validators: tuple[ValidationRule, ...],
    ) -> None:
        if any(not isinstance(item, ValidationRule) for item in validators):
            raise TypeError("validators must contain ValidationRule objects")
        identities = [id(item) for item in validators]
        if len(identities) != len(set(identities)):
            raise ValueError("validators must not contain the same object twice")

    @staticmethod
    def _validate_descriptor_rules(
        descriptor_rules: tuple[DescriptorUseRule, ...],
    ) -> None:
        if any(not isinstance(item, DescriptorUseRule) for item in descriptor_rules):
            raise TypeError("descriptor_rules must contain DescriptorUseRule objects")
        identities = [id(item) for item in descriptor_rules]
        if len(identities) != len(set(identities)):
            raise ValueError("descriptor_rules must not contain the same object twice")

    def recognizes(self, information_type: InformationType[Any]) -> bool:
        """Return whether this Shikumi recognizes an information type by identity."""

        return any(item is information_type for item in self.information_types)

    @staticmethod
    def _focus(
        subject: object | Focus,
        placement: tuple[str, ...] | None,
    ) -> Focus:
        if isinstance(subject, Focus):
            if placement is not None:
                raise ValueError(
                    "placement must be supplied either by Focus or by the method, not both"
                )
            return subject
        return Focus(subject, placement=placement)

    def view(
        self,
        subject: object | Focus,
        *,
        placement: tuple[str, ...] | None = None,
    ) -> SemanticView:
        """Interpret *subject* and return its semantic view."""

        focus = self._focus(subject, placement)
        resolved = self.structure.resolve(focus)
        items = tuple(
            ViewItem(
                node=node,
                information=select_information(node.subject, self.information_types),
                descriptor_uses=descriptor_uses_of(node.subject),
            )
            for node in resolved.nodes
        )
        return SemanticView(focus=focus, structure=resolved, items=items)

    def derive_structure_specification(
        self,
        subject: object | Focus,
        *,
        placement: tuple[str, ...] | None = None,
    ) -> StructureSpecification:
        """Derive a root-relative structural regulation from a description body."""

        view = self.view(subject, placement=placement)
        return StructureSpecification.from_resolved(view.structure)

    def validate(
        self,
        subject: object | Focus,
        *,
        placement: tuple[str, ...] | None = None,
        structure_specification: StructureSpecification | None = None,
    ) -> ValidationResult:
        """Validate *subject* with rules and an optional structural regulation.

        A standalone module requires an explicit placement. This makes its
        intended structural context part of the validation request instead of
        silently using its current import path as the premise.
        """

        focus = self._focus(subject, placement)
        if (
            isinstance(focus.subject, ModuleType)
            and not hasattr(focus.subject, "__path__")
            and focus.placement is None
        ):
            raise ValueError("standalone module validation requires an explicit placement")

        root_view = self.view(focus)
        diagnostics: list[Diagnostic] = []

        for item in root_view.items:
            applicable = tuple(
                rule for rule in self.validators if rule.focus_kind is item.kind
            )
            if not applicable:
                continue

            rule_view = (
                root_view
                if item.subject is root_view.focus.subject
                else root_view.subview(item.subject)
            )
            for rule in applicable:
                diagnostics.extend(rule(rule_view))

        diagnostics.extend(check_descriptor_uses(root_view, self.descriptor_rules))

        structure_result = None
        if structure_specification is not None:
            structure_result = check_structure(
                root_view.structure,
                structure_specification,
            )
            diagnostics.extend(structure_result.diagnostics)

        return ValidationResult(
            view=root_view,
            diagnostics=tuple(diagnostics),
            structure_check=structure_result,
        )
