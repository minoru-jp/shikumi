"""Command-line interface for composing Shikumi runtime components."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from ._cli.artifact import write_artifact
from ._cli.loading import (
    is_standalone_module,
    load_realizer,
    load_reference,
    load_shikumi,
    parse_placement,
    select_structure,
)
from ._cli.payload import error_payload, realization_payload, validation_payload
from ._cli.rendering import (
    emit,
    render_error_text,
    render_realization_text,
    render_validation_text,
)
from ._cli.types import CLIError
from .realization import RealizationCheck


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="shikumi",
        description="Interpret, validate, and realize Python runtime descriptions.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate",
        help="validate a Python module, package, or object with a Shikumi",
    )
    _add_common_arguments(validate_parser)
    structure_group = validate_parser.add_mutually_exclusive_group()
    structure_group.add_argument(
        "--structure-spec",
        metavar="MODULE:OBJECT",
        help="explicit StructureSpecification published by a regulation body",
    )
    structure_group.add_argument(
        "--structure-from",
        metavar="MODULE[:OBJECT]",
        help="derive the structural regulation from this description body",
    )
    validate_parser.add_argument(
        "--realizer",
        metavar="MODULE:OBJECT",
        help="also query whether this Realizer can realize the semantic view",
    )

    realize_parser = subparsers.add_parser(
        "realize",
        help="realize a Python module, package, or object through a semantic view",
    )
    _add_common_arguments(realize_parser)
    realize_parser.add_argument(
        "--realizer",
        required=True,
        metavar="MODULE:OBJECT",
        help="Python reference to a Realizer instance",
    )
    realize_parser.add_argument(
        "--output",
        required=True,
        metavar="PATH",
        help="artifact output path; CLI status remains on stdout",
    )

    return parser


def _add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--shikumi",
        required=True,
        metavar="MODULE:OBJECT",
        help="Python reference to a Shikumi instance",
    )
    parser.add_argument(
        "--body",
        required=True,
        metavar="MODULE[:OBJECT]",
        help="Python module/package or object used as the description body",
    )
    parser.add_argument(
        "--at",
        metavar="PLACEMENT",
        help="intended structural placement, written as a dotted path; '.' means root",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="CLI response format (default: text)",
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Run the Shikumi command-line interface and return a process exit code."""

    parser = _parser()
    args = parser.parse_args(argv)
    command: str = args.command
    output_format: str = args.format

    try:
        shikumi = load_shikumi(args.shikumi)
        body = load_reference(args.body, require_object=False)
        placement = parse_placement(args.at)

        if command == "validate":
            if is_standalone_module(body) and placement is None:
                raise CLIError(
                    "placement_required",
                    "standalone module validation requires --at to state its intended placement",
                )

            structure = select_structure(args, shikumi)
            try:
                result = shikumi.validate(
                    body,
                    placement=placement,
                    structure_specification=(
                        structure.specification if structure is not None else None
                    ),
                )
            except Exception as exc:
                raise CLIError(
                    "validation_error", str(exc) or type(exc).__name__
                ) from exc

            realization: tuple[str, RealizationCheck] | None = None
            if args.realizer is not None:
                realizer = load_realizer(args.realizer)
                try:
                    check = realizer.check(result.view)
                except Exception as exc:
                    raise CLIError(
                        "realizability_error", str(exc) or type(exc).__name__
                    ) from exc
                if not isinstance(check, RealizationCheck):
                    raise CLIError(
                        "type_error",
                        f"{args.realizer!r}.check() did not return RealizationCheck",
                    )
                realization = (args.realizer, check)

            payload = validation_payload(
                result,
                shikumi_reference=args.shikumi,
                body_reference=args.body,
                placement_reference=args.at,
                structure=structure,
                realization=realization,
            )
            emit(
                payload,
                output_format=output_format,
                text=render_validation_text(payload),
            )
            return 0 if bool(payload["ok"]) else 1

        if command == "realize":
            realizer = load_realizer(args.realizer)
            try:
                view = shikumi.view(body, placement=placement)
            except Exception as exc:
                raise CLIError(
                    "interpretation_error", str(exc) or type(exc).__name__
                ) from exc
            try:
                artifact = realizer.realize(view)
            except Exception as exc:
                raise CLIError(
                    "realization_error", str(exc) or type(exc).__name__
                ) from exc
            write = write_artifact(artifact, args.output)
            payload = realization_payload(
                shikumi_reference=args.shikumi,
                body_reference=args.body,
                placement_reference=args.at,
                realizer_reference=args.realizer,
                write=write,
            )
            emit(
                payload,
                output_format=output_format,
                text=render_realization_text(payload),
            )
            return 0

        raise AssertionError(f"unhandled command: {command}")

    except CLIError as error:
        payload = error_payload(command, error)
        emit(
            payload,
            output_format=output_format,
            text=render_error_text(error),
        )
        return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
