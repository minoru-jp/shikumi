"""Text and JSON rendering for CLI response payloads."""

from __future__ import annotations

import json

from .types import CLIError, RealizationPayload, ValidationPayload


def render_validation_text(payload: ValidationPayload) -> str:
    counts = payload["diagnostic_counts"]
    diagnostics = payload["diagnostics"]

    lines = [
        "Validation succeeded" if payload["ok"] else "Validation failed",
        f"Shikumi: {payload['shikumi']}",
        f"Body: {payload['body']}",
        f"Focus: {payload['focus_kind']}",
    ]
    if payload["placement"] is not None:
        lines.append(f"Placement: {payload['placement']}")

    structure = payload["structure"]
    if structure is not None:
        state = "succeeded" if structure["ok"] else "failed"
        lines.append(
            f"Structure: {state} ({structure['mode']}: {structure['reference']})"
        )

    realization = payload["realization"]
    if realization is not None:
        state = "realizable" if realization["ok"] else "not realizable"
        lines.append(f"Realizer: {state} ({realization['realizer']})")

    lines.append(
        "Diagnostics: "
        f"{counts['error']} error, {counts['warning']} warning, {counts['info']} info"
    )
    if diagnostics:
        lines.append("")
    for item in diagnostics:
        severity = item["severity"].upper()
        code = item["code"]
        subject = item["subject"]
        header = severity
        if code is not None:
            header += f" [{code}]"
        if subject is not None:
            header += f" {subject}"
        lines.append(header)
        lines.append(f"  {item['message']}")

    if realization is not None:
        rdiagnostics = realization["diagnostics"]
        rcounts = realization["diagnostic_counts"]
        lines.append(
            "Realizability diagnostics: "
            f"{rcounts['error']} error, {rcounts['warning']} warning, {rcounts['info']} info"
        )
        if rdiagnostics:
            lines.append("")
        for item in rdiagnostics:
            severity = item["severity"].upper()
            code = item["code"]
            subject = item["subject"]
            header = severity
            if code is not None:
                header += f" [{code}]"
            if subject is not None:
                header += f" {subject}"
            lines.append(header)
            lines.append(f"  {item['message']}")

    return "\n".join(lines) + "\n"


def render_realization_text(payload: RealizationPayload) -> str:
    artifact = payload["artifact"]
    lines = [
        "Realization succeeded",
        f"Shikumi: {payload['shikumi']}",
        f"Body: {payload['body']}",
    ]
    if payload["placement"] is not None:
        lines.append(f"Placement: {payload['placement']}")
    lines.extend(
        [
            f"Realizer: {payload['realizer']}",
            f"Output: {artifact['output']}",
            f"Artifact: {artifact['kind']}",
        ]
    )
    return "\n".join(lines) + "\n"


def render_error_text(error: CLIError) -> str:
    return f"Error [{error.error_type}]: {error.message}\n"


def emit(payload: object, *, output_format: str, text: str) -> None:
    if output_format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False))
    else:
        print(text, end="")
