from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    value = str(path)
    if value not in sys.path:
        sys.path.insert(0, value)

from shikumi_devdoc.cli import main as devdoc_main


CANONICAL_DOCUMENTS = ROOT / "devdocs" / "canonical_documents"
NOTICE_PATH = ROOT / "devdocs" / "config" / "notice.toml"

# kind, canonical source module, output directory/file, expected relative output
DOCUMENT_ARTIFACTS: tuple[tuple[str, str, Path, Path], ...] = (
    ("document", "devdocs.canonical_sources.readme", Path("."), Path("README.md")),
    ("document", "devdocs.canonical_sources.changelog", Path("."), Path("CHANGELOG.md")),
    ("document", "devdocs.canonical_sources.status", Path("."), Path("STATUS.md")),
    ("glossary", "devdocs.canonical_sources.docs.vocabulary", Path("docs/glossary.md"), Path("docs/glossary.md")),
    ("document", "devdocs.canonical_sources.docs.guides.getting_started", Path("docs/guides"), Path("docs/guides/getting-started.md")),
    ("document", "devdocs.canonical_sources.docs.guides.descriptor_authoring", Path("docs/guides"), Path("docs/guides/descriptor-authoring.md")),
    ("document", "devdocs.canonical_sources.docs.guides.project_layout", Path("docs/guides"), Path("docs/guides/project-layout.md")),
    ("document", "devdocs.canonical_sources.devdocs.readme", Path("devdocs"), Path("devdocs/README.md")),
    ("document", "devdocs.canonical_sources.examples.structure_showcase.canonical", Path("examples/structure_showcase"), Path("examples/structure_showcase/README.md")),
    ("document", "devdocs.canonical_sources.docs.api.information", Path("docs/api"), Path("docs/api/information.md")),
    ("document", "devdocs.canonical_sources.docs.api.descriptors", Path("docs/api"), Path("docs/api/descriptors.md")),
    ("document", "devdocs.canonical_sources.docs.api.structure", Path("docs/api"), Path("docs/api/structure.md")),
    ("document", "devdocs.canonical_sources.docs.api.semantic_view", Path("docs/api"), Path("docs/api/semantic-view.md")),
    ("document", "devdocs.canonical_sources.docs.api.shikumi", Path("docs/api"), Path("docs/api/shikumi.md")),
    ("document", "devdocs.canonical_sources.docs.api.validation", Path("docs/api"), Path("docs/api/validation.md")),
    ("document", "devdocs.canonical_sources.docs.api.realization", Path("docs/api"), Path("docs/api/realization.md")),
    ("document", "devdocs.canonical_sources.docs.api.standard", Path("docs/api"), Path("docs/api/standard.md")),
    ("document", "devdocs.canonical_sources.docs.api.errors", Path("docs/api"), Path("docs/api/errors.md")),
    ("document", "devdocs.canonical_sources.docs.api.cli", Path("docs/api"), Path("docs/api/cli.md")),
    ("document", "devdocs.canonical_sources.docs.specification.core", Path("docs/specification"), Path("docs/specification/core.md")),
    ("document", "devdocs.canonical_sources.docs.specification.description", Path("docs/specification"), Path("docs/specification/description.md")),
    ("document", "devdocs.canonical_sources.docs.specification.structure", Path("docs/specification"), Path("docs/specification/structure.md")),
    ("document", "devdocs.canonical_sources.docs.specification.validation", Path("docs/specification"), Path("docs/specification/validation.md")),
    ("document", "devdocs.canonical_sources.docs.specification.realization", Path("docs/specification"), Path("docs/specification/realization.md")),
    ("document", "devdocs.canonical_sources.docs.specification.public_api", Path("docs/specification"), Path("docs/specification/public-api.md")),
    ("document", "devdocs.canonical_sources.docs.specification.cli", Path("docs/specification"), Path("docs/specification/cli.md")),
)

# canonical source package, output directory, expected relative output, index title
INDEX_ARTIFACTS: tuple[tuple[str, Path, Path, str], ...] = (
    ("devdocs.canonical_sources.docs.guides", Path("docs/guides"), Path("docs/guides/INDEX.md"), "Shikumi Guides"),
    ("devdocs.canonical_sources.docs.api", Path("docs/api"), Path("docs/api/INDEX.md"), "Shikumi API Reference"),
    ("devdocs.canonical_sources.docs.specification", Path("docs/specification"), Path("docs/specification/INDEX.md"), "Shikumi Specification"),
)


def _project_context() -> str:
    with (ROOT / "pyproject.toml").open("rb") as stream:
        project = tomllib.load(stream)["project"]

    scripts = project.get("scripts", {})
    cli_entry_point = next(iter(scripts), project["name"])
    context = {
        "PROJECT": {
            "name": project["name"],
            "version": project["version"],
            "requires_python": project["requires-python"],
            "distribution": project["name"],
            "import_package": "shikumi",
            "cli_entry_point": cli_entry_point,
        }
    }
    return json.dumps(context, ensure_ascii=False, separators=(",", ":"))


def _run(argv: list[str]) -> None:
    exit_code = devdoc_main(argv)
    if exit_code != 0:
        raise SystemExit(exit_code)


def _base_render_args(kind: str, module: str, output: Path, context: str) -> list[str]:
    return [
        "render",
        kind,
        module,
        "-o",
        str(output),
        "--context",
        context,
        "--notice",
        str(NOTICE_PATH),
        "--translation-source",
    ]


def _render_all(output_root: Path) -> None:
    context = _project_context()
    for kind, module, relative_output, _ in DOCUMENT_ARTIFACTS:
        _run(_base_render_args(kind, module, output_root / relative_output, context))

    for module, relative_output, _, index_title in INDEX_ARTIFACTS:
        argv = _base_render_args("index", module, output_root / relative_output, context)
        argv.extend(["--index-title", index_title])
        _run(argv)


def _files_under(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def _expected_files() -> set[Path]:
    return {
        *(artifact[3] for artifact in DOCUMENT_ARTIFACTS),
        *(artifact[2] for artifact in INDEX_ARTIFACTS),
    }


def _check() -> None:
    with tempfile.TemporaryDirectory(prefix="shikumi-docs-") as raw_temp:
        temp_root = Path(raw_temp) / "canonical_documents"
        _render_all(temp_root)

        expected_files = _expected_files()
        actual_files = _files_under(CANONICAL_DOCUMENTS)
        rendered_files = _files_under(temp_root)
        mismatches = sorted(
            (expected_files ^ actual_files)
            | (expected_files ^ rendered_files)
            | {
                path
                for path in expected_files & actual_files & rendered_files
                if (CANONICAL_DOCUMENTS / path).read_bytes()
                != (temp_root / path).read_bytes()
            }
        )

    if mismatches:
        rendered = "\n".join(f"  - {path.as_posix()}" for path in mismatches)
        raise SystemExit(
            "canonical documents are out of date:\n"
            f"{rendered}\n"
            "run `python scripts/render_canonical_docs.py` and commit the results"
        )
    print("canonical documents are up to date")


def _write() -> None:
    if CANONICAL_DOCUMENTS.exists():
        shutil.rmtree(CANONICAL_DOCUMENTS)
    CANONICAL_DOCUMENTS.mkdir(parents=True)
    _render_all(CANONICAL_DOCUMENTS)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate committed Japanese canonical documents with shikumi-devdoc."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed canonical documents without modifying them",
    )
    args = parser.parse_args()
    if args.check:
        _check()
    else:
        _write()


if __name__ == "__main__":
    main()
