"""Shared internal CLI value types."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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


class CLIError(Exception):
    def __init__(self, error_type: str, message: str) -> None:
        super().__init__(message)
        self.error_type = error_type
        self.message = message
