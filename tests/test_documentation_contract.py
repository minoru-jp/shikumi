from __future__ import annotations

import re
from pathlib import Path

import shikumi
import shikumi.standard


_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _public_markdown_files() -> list[Path]:
    files = [Path("README.md"), Path("STATUS.md"), Path("CHANGELOG.md")]
    files.extend(sorted(Path("docs").rglob("*.md")))
    files.extend(sorted(Path("examples").glob("*/README.md")))
    return files


def test_public_relative_markdown_links_resolve() -> None:
    missing: list[tuple[Path, str]] = []
    for path in _public_markdown_files():
        text = path.read_text(encoding="utf-8")
        for target in _LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            raw = target.split("#", 1)[0]
            if not raw:
                continue
            resolved = (path.parent / raw).resolve()
            if not resolved.exists():
                missing.append((path, target))
    assert not missing, missing


def test_every_exported_python_api_name_is_present_in_api_reference_collection() -> None:
    api_text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(Path("docs/api").glob("*.md"))
    )
    for name in (*shikumi.__all__, *shikumi.standard.__all__):
        assert f"`{name}" in api_text or f"name: {name}" in api_text, name


def _relative_md_targets(path: Path) -> tuple[str, ...]:
    return tuple(
        target.split("#", 1)[0]
        for target in _LINK.findall(path.read_text(encoding="utf-8"))
        if target.split("#", 1)[0].endswith(".md")
    )


def test_published_collection_topology_matches_canonical_collection_indexes() -> None:
    pairs = (
        (
            Path("devdocs/canonical_documents/docs/guides/INDEX.md"),
            Path("docs/guides/INDEX.md"),
        ),
        (
            Path("devdocs/canonical_documents/docs/api/INDEX.md"),
            Path("docs/api/INDEX.md"),
        ),
        (
            Path("devdocs/canonical_documents/docs/specification/INDEX.md"),
            Path("docs/specification/INDEX.md"),
        ),
    )
    for canonical, published in pairs:
        assert _relative_md_targets(published) == _relative_md_targets(canonical)


def _api_name_values() -> set[str]:
    from shikumi_devdoc.norms._document import DocumentField, FieldValue
    from shikumi_devdoc.norms.document import system as document_system
    from devdocs.canonical_sources.docs.api import cli, descriptors, errors, information
    from devdocs.canonical_sources.docs.api import realization, semantic_view, shikumi as shikumi_doc
    from devdocs.canonical_sources.docs.api import standard, structure, validation

    modules = (
        information,
        descriptors,
        structure,
        semantic_view,
        shikumi_doc,
        validation,
        realization,
        standard,
        errors,
        cli,
    )
    values: set[str] = set()
    for module in modules:
        result = document_system.validate(module, placement=())
        assert result.is_valid, (module.__name__, result.diagnostics)
        for item in result.view.items:
            for value in item.values(DocumentField):
                if (
                    isinstance(value, FieldValue)
                    and value.binding_name == "name"
                    and isinstance(value.value, str)
                ):
                    values.add(value.value)
    return values


def _api_subject_base(name: str) -> str:
    return name.split("(", 1)[0].strip()


def test_each_exported_python_api_has_its_own_api_subject() -> None:
    names = _api_name_values()
    assert not {name for name in names if " / " in name}
    documented_bases = {_api_subject_base(name) for name in names}
    for exported in (*shikumi.__all__, *shikumi.standard.__all__):
        assert exported in documented_bases, exported


def _document_structure_signature(path: Path) -> tuple[str, ...]:
    field = re.compile(
        r"^(name|kind|input|output|level|title|condition|detail|related|"
        r"introduced|deprecated|removed|replacement|migration):"
    )
    heading = re.compile(r"^(#{1,6}) ")
    signature: list[str] = []
    in_fence = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = heading.match(line)
        if match:
            signature.append(f"H{len(match.group(1))}")
            continue
        match = field.match(line)
        if match:
            signature.append(f"F:{match.group(1)}")
    return tuple(signature)


def test_published_api_and_specification_preserve_canonical_structure() -> None:
    canonical_root = Path("devdocs/canonical_documents")
    for collection in ("api", "specification"):
        for canonical in sorted((canonical_root / "docs" / collection).glob("*.md")):
            if canonical.name == "INDEX.md":
                continue
            published = Path("docs") / collection / canonical.name
            assert published.is_file(), published
            assert _document_structure_signature(published) == _document_structure_signature(
                canonical
            ), published
