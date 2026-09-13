"""Python reference and structural-context loading for the CLI."""

from __future__ import annotations

import argparse
import importlib
from types import ModuleType
from typing import Any

from ..model import Shikumi
from ..realization import Realizer
from ..structure import StructureSpecification
from .types import CLIError, StructureSelection


def load_reference(reference: str, *, require_object: bool) -> object:
    module_name, separator, object_path = reference.partition(":")
    if not module_name:
        raise CLIError("reference_error", f"invalid Python reference: {reference!r}")
    if require_object and not separator:
        raise CLIError(
            "reference_error",
            f"Python reference must name an object with 'module:object': {reference!r}",
        )
    if separator and not object_path:
        raise CLIError("reference_error", f"missing object name in reference: {reference!r}")

    try:
        value: object = importlib.import_module(module_name)
    except Exception as exc:
        raise CLIError(
            "import_error",
            f"could not import module {module_name!r}: {exc}",
        ) from exc

    if not separator:
        return value

    for name in object_path.split("."):
        try:
            value = getattr(value, name)
        except AttributeError as exc:
            raise CLIError(
                "reference_error",
                f"reference {reference!r} has no object component {name!r}",
            ) from exc
    return value


def load_shikumi(reference: str) -> Shikumi:
    value = load_reference(reference, require_object=True)
    if not isinstance(value, Shikumi):
        raise CLIError(
            "type_error",
            f"{reference!r} does not resolve to a Shikumi instance",
        )
    return value


def load_realizer(reference: str) -> Realizer[Any]:
    value = load_reference(reference, require_object=True)
    if not isinstance(value, Realizer):
        raise CLIError(
            "type_error",
            f"{reference!r} does not resolve to a Realizer instance",
        )
    return value


def load_structure_specification(reference: str) -> StructureSpecification:
    value = load_reference(reference, require_object=True)
    if not isinstance(value, StructureSpecification):
        raise CLIError(
            "type_error",
            f"{reference!r} does not resolve to a StructureSpecification",
        )
    return value


def parse_placement(value: str | None) -> tuple[str, ...] | None:
    if value is None:
        return None
    if value == ".":
        return ()
    parts = tuple(value.split("."))
    if any(not part for part in parts):
        raise CLIError(
            "placement_error",
            f"invalid structural placement: {value!r}",
        )
    return parts


def is_standalone_module(subject: object) -> bool:
    return isinstance(subject, ModuleType) and not hasattr(subject, "__path__")


def select_structure(
    args: argparse.Namespace,
    shikumi: Shikumi,
) -> StructureSelection | None:
    if args.structure_spec is not None:
        return StructureSelection(
            mode="explicit",
            reference=args.structure_spec,
            specification=load_structure_specification(args.structure_spec),
        )

    if args.structure_from is not None:
        source = load_reference(args.structure_from, require_object=False)
        if not isinstance(source, ModuleType):
            raise CLIError(
                "type_error",
                f"{args.structure_from!r} does not resolve to a module or package description body",
            )
        try:
            specification = shikumi.derive_structure_specification(source)
        except Exception as exc:
            raise CLIError(
                "structure_derivation_error",
                str(exc) or type(exc).__name__,
            ) from exc
        return StructureSelection(
            mode="derived",
            reference=args.structure_from,
            specification=specification,
        )

    return None
