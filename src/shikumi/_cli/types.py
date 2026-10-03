"""Shared internal CLI value types."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, TypedDict

from ..structure import StructureSpecification


@dataclass(frozen=True, slots=True)
class ArtifactWrite:
    path: Path
    kind: str


@dataclass(frozen=True, slots=True)
class StructureSelection:
    mode: str
    reference: str
    specification: StructureSpecification


class CLIArguments(Protocol):
    """Typed view of the attributes populated by the CLI parser."""

    @property
    def command(self) -> str: ...

    @property
    def format(self) -> str: ...

    @property
    def shikumi(self) -> str: ...

    @property
    def body(self) -> str: ...

    @property
    def at(self) -> str | None: ...

    @property
    def structure_spec(self) -> str | None: ...

    @property
    def structure_from(self) -> str | None: ...

    @property
    def realizer(self) -> str | None: ...

    @property
    def output(self) -> str: ...


class DiagnosticCountsPayload(TypedDict):
    error: int
    warning: int
    info: int


class DiagnosticPayload(TypedDict):
    severity: str
    code: str | None
    message: str
    subject: str | None


class StructurePayload(TypedDict):
    mode: str
    reference: str
    ok: bool
    placement: str


class RealizabilityPayload(TypedDict):
    realizer: str
    ok: bool
    diagnostic_counts: DiagnosticCountsPayload
    diagnostics: list[DiagnosticPayload]


class ValidationPayload(TypedDict):
    format_version: int
    command: Literal["validate"]
    ok: bool
    shikumi: str
    body: str
    focus_kind: str
    placement: str | None
    diagnostic_counts: DiagnosticCountsPayload
    diagnostics: list[DiagnosticPayload]
    structure: StructurePayload | None
    realization: RealizabilityPayload | None


class ArtifactPayload(TypedDict):
    output: str
    kind: str


class RealizationPayload(TypedDict):
    format_version: int
    command: Literal["realize"]
    ok: bool
    shikumi: str
    body: str
    placement: str | None
    realizer: str
    artifact: ArtifactPayload


class ErrorDetailsPayload(TypedDict):
    type: str
    message: str


class ErrorPayload(TypedDict):
    format_version: int
    command: str | None
    ok: bool
    error: ErrorDetailsPayload


class CLIError(Exception):
    error_type: str
    message: str

    def __init__(self, error_type: str, message: str) -> None:
        super().__init__(message)
        self.error_type = error_type
        self.message = message
