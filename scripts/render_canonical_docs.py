from __future__ import annotations

import argparse
import json
from pathlib import Path
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


BUILD_ROOT = ROOT / "_internal" / "document_build" / "ja"
TERMS_PATH = ROOT / "_internal" / "document_source" / "vocabulary" / "terms.py"
NOTICE_PATH = ROOT / "_internal" / "document_source" / "notice.toml"
VOCABULARY_MODULE = "_internal.document_source.vocabulary.canonical"

DOCUMENTS: tuple[tuple[str, str, Path], ...] = (
    ("document", "_internal.document_source.readme.canonical", Path("README.md")),
    ("changelog", "_internal.document_source.changelog", Path("CHANGELOG.md")),
    ("glossary", VOCABULARY_MODULE, Path("docs/glossary.md")),
    ("document", "_internal.document_source.api_reference.canonical", Path("docs/api-reference.md")),
    ("document", "_internal.document_source.distribution_guide.canonical", Path("docs/distribution-guide.md")),
    ("document", "_internal.document_source.documentation_workflow.canonical", Path("DOCUMENTATION_WORKFLOW.md")),
    ("document", "_internal.document_source.examples.architecture.canonical", Path("examples/architecture/README.md")),
    ("document", "_internal.document_source.examples.structured_docs.canonical", Path("examples/structured_docs/README.md")),
    ("document", "_internal.document_source.examples.web_api.canonical", Path("examples/web_api/README.md")),
    ("document", "_internal.document_source.examples.structure_from_body.canonical", Path("examples/structure_from_body/README.md")),
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


def _generate_terms(output: Path) -> None:
    _run(["terms", VOCABULARY_MODULE, "-o", str(output)])


def _render_documents(output_root: Path) -> None:
    context = _project_context()
    for kind, module, relative_output in DOCUMENTS:
        output = output_root / relative_output
        _run([
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
        ])


def _same_bytes(expected: Path, actual: Path) -> bool:
    return expected.is_file() and expected.read_bytes() == actual.read_bytes()


def _check() -> None:
    mismatches: list[Path] = []
    with tempfile.TemporaryDirectory(prefix="shikumi-docs-") as raw_temp:
        temp = Path(raw_temp)
        temp_terms = temp / "terms.py"
        _generate_terms(temp_terms)
        if not _same_bytes(TERMS_PATH, temp_terms):
            mismatches.append(TERMS_PATH.relative_to(ROOT))
            # Document sources import the committed terms module. Stop here so a
            # stale term-reference module cannot obscure the primary drift.
        else:
            temp_build = temp / "build"
            _render_documents(temp_build)
            for _, _, relative_output in DOCUMENTS:
                expected = BUILD_ROOT / relative_output
                actual = temp_build / relative_output
                if not _same_bytes(expected, actual):
                    mismatches.append(expected.relative_to(ROOT))

    if mismatches:
        rendered = "\n".join(f"  - {path.as_posix()}" for path in mismatches)
        raise SystemExit(
            "generated developer documentation is out of date:\n"
            f"{rendered}\n"
            "run `python scripts/render_canonical_docs.py` and commit the results"
        )
    print("developer documentation is up to date")


def _write() -> None:
    _generate_terms(TERMS_PATH)
    _render_documents(BUILD_ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate committed Japanese documentation intermediates with shikumi-devdoc."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify committed term references and intermediates without modifying them",
    )
    args = parser.parse_args()
    if args.check:
        _check()
    else:
        _write()


if __name__ == "__main__":
    main()
