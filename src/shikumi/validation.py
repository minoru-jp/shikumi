"""Validation of semantic views around explicit runtime foci."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, replace
from enum import Enum
from typing import TypeAlias

from .description import DescriptorUseRule, same_descriptor
from .structure import (
    Focus,
    ResolvedStructure,
    StructuralKind,
    StructureSpecification,
)
from .view import SemanticView


class DiagnosticSeverity(str, Enum):
    """Severity attached to one validation diagnostic."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """One reportable observation produced by validation."""

    message: str
    code: str | None = None
    severity: DiagnosticSeverity = DiagnosticSeverity.ERROR
    subject: object | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.message, str):
            raise TypeError("diagnostic message must be a string")
        if not self.message:
            raise ValueError("diagnostic message must not be empty")
        if self.code is not None and not isinstance(self.code, str):
            raise TypeError("diagnostic code must be a string or None")
        if self.code == "":
            raise ValueError("diagnostic code must not be empty")
        if not isinstance(self.severity, DiagnosticSeverity):
            raise TypeError("diagnostic severity must be a DiagnosticSeverity")


ValidationOutput: TypeAlias = Diagnostic | Iterable[Diagnostic] | None
ValidationFunction: TypeAlias = Callable[[SemanticView], ValidationOutput]


@dataclass(frozen=True, slots=True, eq=False)
class ValidationRule:
    """A condition evaluated with a semantic view of one required focus kind.

    Rules are identity-based. The rule declares the kind of focus it needs;
    validation decides which runtime subjects can naturally provide that focus.
    """

    focus_kind: StructuralKind
    check: ValidationFunction
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.focus_kind, StructuralKind):
            raise TypeError("validation rule focus_kind must be a StructuralKind")
        if not callable(self.check):
            raise TypeError("validation rule check must be callable")
        if not isinstance(self.name, str):
            raise TypeError("validation rule name must be a string")
        if not self.name:
            raise ValueError("validation rule name must not be empty")

    def __call__(self, view: SemanticView) -> tuple[Diagnostic, ...]:
        """Evaluate this rule against a view with the required focused kind."""

        if view.focused.kind is not self.focus_kind:
            raise ValueError(
                f"validation rule {self.name!r} requires focus kind "
                f"{self.focus_kind.value!r}, got {view.focused.kind.value!r}"
            )

        output = self.check(view)
        return tuple(self._normalize_output(output, view.focus))

    @staticmethod
    def _normalize_output(
        output: ValidationOutput,
        focus: Focus,
    ) -> Iterator[Diagnostic]:
        if output is None:
            return

        if isinstance(output, Diagnostic):
            yield ValidationRule._bind_subject(output, focus)
            return

        for diagnostic in output:
            if not isinstance(diagnostic, Diagnostic):
                raise TypeError("validation rules must yield Diagnostic objects")
            yield ValidationRule._bind_subject(diagnostic, focus)

    @staticmethod
    def _bind_subject(diagnostic: Diagnostic, focus: Focus) -> Diagnostic:
        if diagnostic.subject is not None:
            return diagnostic
        return replace(diagnostic, subject=focus.subject)


@dataclass(frozen=True, slots=True)
class StructureCheck:
    """Result of checking a resolved structure against a structural regulation."""

    specification: StructureSpecification
    placement: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def is_valid(self) -> bool:
        return not any(
            diagnostic.severity is DiagnosticSeverity.ERROR
            for diagnostic in self.diagnostics
        )

    def __bool__(self) -> bool:
        return self.is_valid


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Diagnostics produced while validating one requested focus."""

    view: SemanticView
    diagnostics: tuple[Diagnostic, ...]
    structure_check: StructureCheck | None = None

    @property
    def is_valid(self) -> bool:
        """Return whether validation produced no error diagnostics."""

        return not any(
            diagnostic.severity is DiagnosticSeverity.ERROR
            for diagnostic in self.diagnostics
        )

    def __bool__(self) -> bool:
        return self.is_valid


def _effective_path(view: SemanticView, node_path: tuple[str, ...]) -> tuple[str, ...]:
    """Return a regulation-root-relative path for one node in *view*."""

    root_path = view.focused.node.path
    if node_path[: len(root_path)] != root_path:
        raise ValueError("semantic view contains a node outside its focus root")
    relative = node_path[len(root_path) :]
    if view.focus.placement is not None:
        return view.focus.placement + relative
    return relative


def check_descriptor_uses(
    view: SemanticView,
    rules: Iterable[DescriptorUseRule],
) -> tuple[Diagnostic, ...]:
    """Check recorded descriptor uses against structural usage rules."""

    normalized_rules = tuple(rules)
    diagnostics: list[Diagnostic] = []
    for item in view.items:
        path = _effective_path(view, item.node.path)
        for use in item.descriptor_uses:
            for rule in normalized_rules:
                if not same_descriptor(use.descriptor, rule.descriptor):
                    continue
                if not rule.allowed.matches(kind=item.kind, path=path):
                    diagnostics.append(
                        Diagnostic(
                            f"descriptor {rule.display_name!r} cannot be used at "
                            f"{StructureSpecification.format_path(path)} "
                            f"({item.kind.value})",
                            code="descriptor.use.disallowed",
                            subject=item.subject,
                        )
                    )
                    continue
                if rule.recommended is not None and not rule.recommended.matches(
                    kind=item.kind,
                    path=path,
                ):
                    diagnostics.append(
                        Diagnostic(
                            f"descriptor {rule.display_name!r} is allowed but not "
                            f"recommended at {StructureSpecification.format_path(path)} "
                            f"({item.kind.value})",
                            code="descriptor.use.not_recommended",
                            severity=DiagnosticSeverity.WARNING,
                            subject=item.subject,
                        )
                    )
    return tuple(diagnostics)


def check_structure(
    structure: ResolvedStructure,
    specification: StructureSpecification,
) -> StructureCheck:
    """Check one resolved focus against the matching specification subtree.

    The specification is root-relative. If the focus has an explicit
    ``placement``, that path selects the specification subtree to check. If no
    placement is supplied, the focus is treated as the specification root.
    Only the selected subtree is checked, allowing a standalone module to be
    validated at an explicitly stated future position without pretending that
    its siblings were also observed.
    """

    root = structure.node_for(structure.focus.subject)
    if root is None:  # defensive; ResolvedStructure already guarantees this
        raise ValueError("resolved structure has no focus node")

    placement = structure.focus.placement or ()
    expected_root = specification.element_at(placement)
    if expected_root is None:
        diagnostic = Diagnostic(
            "structure placement is not defined by the specification: "
            f"{StructureSpecification.format_path(placement)}",
            code="structure.placement.undefined",
            subject=structure.focus.subject,
        )
        return StructureCheck(
            specification=specification,
            placement=placement,
            diagnostics=(diagnostic,),
        )

    root_path = root.path
    actual_by_path: dict[tuple[str, ...], object] = {}
    actual_kind_by_path: dict[tuple[str, ...], StructuralKind] = {}
    for node in structure.nodes:
        if node.path[: len(root_path)] != root_path:
            raise ValueError("resolved structure contains a node outside its focus root")
        relative = node.path[len(root_path) :]
        effective = placement + relative
        if effective in actual_kind_by_path:
            raise ValueError(
                "resolved structure contains duplicate path: "
                f"{StructureSpecification.format_path(effective)}"
            )
        actual_by_path[effective] = node.subject
        actual_kind_by_path[effective] = node.kind

    expected = {element.path: element.kind for element in specification.subtree(placement)}
    diagnostics: list[Diagnostic] = []

    for path, expected_kind in expected.items():
        actual_kind = actual_kind_by_path.get(path)
        if actual_kind is None:
            diagnostics.append(
                Diagnostic(
                    "required structural element is missing: "
                    f"{StructureSpecification.format_path(path)} "
                    f"({expected_kind.value})",
                    code="structure.element.missing",
                    subject=structure.focus.subject,
                )
            )
            continue
        if actual_kind is not expected_kind:
            diagnostics.append(
                Diagnostic(
                    "structural kind does not match at "
                    f"{StructureSpecification.format_path(path)}: expected "
                    f"{expected_kind.value}, got {actual_kind.value}",
                    code="structure.kind.mismatch",
                    subject=actual_by_path[path],
                )
            )

    for path, actual_kind in actual_kind_by_path.items():
        if path in expected:
            continue
        diagnostics.append(
            Diagnostic(
                "unexpected structural element: "
                f"{StructureSpecification.format_path(path)} ({actual_kind.value})",
                code="structure.element.unexpected",
                subject=actual_by_path[path],
            )
        )

    return StructureCheck(
        specification=specification,
        placement=placement,
        diagnostics=tuple(diagnostics),
    )


def validator(
    *,
    focus: StructuralKind,
    name: str | None = None,
) -> Callable[[ValidationFunction], ValidationRule]:
    """Create a validation rule from a function.

    The decorated function receives a :class:`SemanticView` centered on the
    declared structural kind and returns or yields :class:`Diagnostic` objects.
    """

    def decorate(function: ValidationFunction) -> ValidationRule:
        rule_name = name if name is not None else function.__name__
        if not rule_name:
            raise ValueError("validation rule name must not be empty")
        return ValidationRule(
            focus_kind=focus,
            check=function,
            name=rule_name,
        )

    return decorate
