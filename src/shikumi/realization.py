"""Independent realization of semantic views into artifacts."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from typing import Generic, TypeVar

from .validation import Diagnostic, DiagnosticSeverity
from .view import SemanticView


ArtifactT = TypeVar("ArtifactT")


@dataclass(frozen=True, slots=True)
class RealizationCheck:
    """Side-effect-free answer to whether one semantic view can be realized."""

    view: SemanticView
    diagnostics: tuple[Diagnostic, ...] = ()

    def __post_init__(self) -> None:
        normalized: list[Diagnostic] = []
        for item in self.diagnostics:
            if not isinstance(item, Diagnostic):
                raise TypeError("realization diagnostics must be Diagnostic objects")
            normalized.append(
                item if item.subject is not None else replace(item, subject=self.view.focus.subject)
            )
        object.__setattr__(self, "diagnostics", tuple(normalized))

    @property
    def is_realizable(self) -> bool:
        """Return whether no error diagnostic prevents realization."""

        return not any(
            diagnostic.severity is DiagnosticSeverity.ERROR
            for diagnostic in self.diagnostics
        )

    def __bool__(self) -> bool:
        return self.is_realizable


class Realizer(ABC, Generic[ArtifactT]):
    """Transforms a semantic view into an artifact.

    A realizer is independent of :class:`Shikumi`: it does not own structure,
    information types, description writers, or validation rules. It consumes
    an already constructed semantic view and may return any Python value as its
    artifact.
    """

    def check(self, view: SemanticView) -> RealizationCheck:
        """Query whether *view* can be realized without producing an artifact.

        Realizers whose realization has preconditions should override this
        method and report them as diagnostics. The default implementation means
        that the realizer declares no additional preconditions.
        """

        return RealizationCheck(view=view)

    @abstractmethod
    def realize(self, view: SemanticView) -> ArtifactT:
        """Produce an artifact from *view*."""
