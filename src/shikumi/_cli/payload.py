"""Stable machine-readable payload construction for the CLI."""

from __future__ import annotations

from types import ModuleType

from ..realization import RealizationCheck
from ..structure import StructureSpecification
from ..validation import Diagnostic, DiagnosticSeverity, ValidationResult
from ..view import SemanticView
from .types import ArtifactWrite, CLIError, StructureSelection


def _subject_name(subject: object) -> str:
    if isinstance(subject, ModuleType):
        return subject.__name__
    module = getattr(subject, "__module__", None)
    qualname = getattr(subject, "__qualname__", None)
    if isinstance(module, str) and isinstance(qualname, str):
        return f"{module}.{qualname}"
    name = getattr(subject, "__name__", None)
    if isinstance(name, str):
        return name
    return type(subject).__name__


def diagnostic_payload(
    view: SemanticView,
    diagnostics_source: tuple[Diagnostic, ...],
) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    for diagnostic in diagnostics_source:
        subject = diagnostic.subject
        path: str | None = None
        if subject is not None:
            node = view.structure.node_for(subject)
            if node is not None:
                path = ".".join(node.path) if node.path else "."
            else:
                path = _subject_name(subject)
        diagnostics.append(
            {
                "severity": diagnostic.severity.value,
                "code": diagnostic.code,
                "message": diagnostic.message,
                "subject": path,
            }
        )
    return diagnostics


def diagnostic_counts(diagnostics: tuple[Diagnostic, ...]) -> dict[str, int]:
    return {
        severity.value: sum(1 for item in diagnostics if item.severity is severity)
        for severity in DiagnosticSeverity
    }


def validation_payload(
    result: ValidationResult,
    *,
    shikumi_reference: str,
    body_reference: str,
    placement_reference: str | None,
    structure: StructureSelection | None,
    realization: tuple[str, RealizationCheck] | None,
) -> dict[str, object]:
    realization_payload: dict[str, object] | None = None
    if realization is not None:
        realizer_reference, check = realization
        realization_payload = {
            "realizer": realizer_reference,
            "ok": check.is_realizable,
            "diagnostic_counts": diagnostic_counts(check.diagnostics),
            "diagnostics": diagnostic_payload(check.view, check.diagnostics),
        }

    structure_payload: dict[str, object] | None = None
    if structure is not None:
        assert result.structure_check is not None
        structure_payload = {
            "mode": structure.mode,
            "reference": structure.reference,
            "ok": result.structure_check.is_valid,
            "placement": StructureSpecification.format_path(
                result.structure_check.placement
            ),
        }

    overall_ok = result.is_valid and (
        realization is None or realization[1].is_realizable
    )
    return {
        "format_version": 1,
        "command": "validate",
        "ok": overall_ok,
        "shikumi": shikumi_reference,
        "body": body_reference,
        "focus_kind": result.view.focused.kind.value,
        "placement": placement_reference,
        "diagnostic_counts": diagnostic_counts(result.diagnostics),
        "diagnostics": diagnostic_payload(result.view, result.diagnostics),
        "structure": structure_payload,
        "realization": realization_payload,
    }


def realization_payload(
    *,
    shikumi_reference: str,
    body_reference: str,
    placement_reference: str | None,
    realizer_reference: str,
    write: ArtifactWrite,
) -> dict[str, object]:
    return {
        "format_version": 1,
        "command": "realize",
        "ok": True,
        "shikumi": shikumi_reference,
        "body": body_reference,
        "placement": placement_reference,
        "realizer": realizer_reference,
        "artifact": {
            "output": str(write.path),
            "kind": write.kind,
        },
    }


def error_payload(command: str | None, error: CLIError) -> dict[str, object]:
    return {
        "format_version": 1,
        "command": command,
        "ok": False,
        "error": {
            "type": error.error_type,
            "message": error.message,
        },
    }
