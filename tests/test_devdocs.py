from __future__ import annotations

import importlib
import re
from pathlib import Path

from shikumi_devdoc.norms.document import system as document_system
from shikumi_devdoc.norms.vocabulary import system as vocabulary_system

DOCUMENT_MODULES = (
    "devdocs.canonical_sources.readme",
    "devdocs.canonical_sources.changelog",
    "devdocs.canonical_sources.docs.guides.getting_started",
    "devdocs.canonical_sources.docs.guides.descriptor_authoring",
    "devdocs.canonical_sources.docs.guides.project_layout",
    "devdocs.canonical_sources.devdocs.readme",
    "devdocs.canonical_sources.examples.structure_showcase.canonical",
    "devdocs.canonical_sources.docs.api.information",
    "devdocs.canonical_sources.docs.api.descriptors",
    "devdocs.canonical_sources.docs.api.structure",
    "devdocs.canonical_sources.docs.api.semantic_view",
    "devdocs.canonical_sources.docs.api.shikumi",
    "devdocs.canonical_sources.docs.api.validation",
    "devdocs.canonical_sources.docs.api.realization",
    "devdocs.canonical_sources.docs.api.errors",
    "devdocs.canonical_sources.docs.api.cli",
    "devdocs.canonical_sources.docs.specification.core",
    "devdocs.canonical_sources.docs.specification.description",
    "devdocs.canonical_sources.docs.specification.structure",
    "devdocs.canonical_sources.docs.specification.validation",
    "devdocs.canonical_sources.docs.specification.realization",
    "devdocs.canonical_sources.docs.specification.public_api",
    "devdocs.canonical_sources.docs.specification.cli",
)


def test_all_canonical_documents_are_valid() -> None:
    for module_name in DOCUMENT_MODULES:
        module = importlib.import_module(module_name)
        result = document_system.validate(module, placement=())
        assert result.is_valid, (module_name, result.diagnostics)


def test_vocabulary_is_valid() -> None:
    module = importlib.import_module("devdocs.canonical_sources.docs.vocabulary")
    result = vocabulary_system.validate(module, placement=())
    assert result.is_valid, result.diagnostics


def test_canonical_documents_have_no_unresolved_project_or_term_placeholders() -> None:
    root = Path("devdocs/canonical_documents")
    assert root.is_dir()
    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        assert "{{TERM_" not in text, path
        assert "{{PROJECT." not in text, path


def test_api_and_specification_collections_use_structured_fields() -> None:
    api = Path("devdocs/canonical_documents/docs/api/information.md").read_text(
        encoding="utf-8"
    )
    spec = Path("devdocs/canonical_documents/docs/specification/core.md").read_text(
        encoding="utf-8"
    )
    assert "name: InformationType" in api
    assert "kind: Type" in api
    assert "input: value: object" in api
    assert "level: MUST" in spec
    assert "title: Runtime state is the source of interpretation" in spec


def test_collection_indexes_are_generated_from_canonical_metadata() -> None:
    guides_index = Path("devdocs/canonical_documents/docs/guides/INDEX.md").read_text(
        encoding="utf-8"
    )
    api_index = Path("devdocs/canonical_documents/docs/api/INDEX.md").read_text(
        encoding="utf-8"
    )
    spec_index = Path(
        "devdocs/canonical_documents/docs/specification/INDEX.md"
    ).read_text(encoding="utf-8")
    assert "[Getting Started](getting-started.md)" in guides_index
    assert "[Project Layout and CLI](project-layout.md)" in guides_index
    assert "[Information API](information.md)" in api_index
    assert "[CLI Reference](cli.md)" in api_index
    assert "[Core Semantics](core.md)" in spec_index
    assert "[CLI Semantics](cli.md)" in spec_index


def test_legacy_devdoc_01_authoring_constructs_are_absent() -> None:
    root = Path("devdocs/canonical_sources")
    source = "\n".join(path.read_text(encoding="utf-8") for path in root.rglob("*.py"))
    assert "vocabulary_refs" not in source
    assert "@vocabulary(terms)" not in source
    assert "shikumi_devdoc.norms.changelog" not in source
    assert "shikumi_devdoc terms" not in source
    assert not Path("devdocs/canonical_sources/docs/terms.py").exists()
    assert not Path("devdocs/canonical_sources/docs/api_reference.py").exists()


def test_current_devdoc_authoring_constructs_are_used() -> None:
    root = Path("devdocs/canonical_sources")
    source = "\n".join(path.read_text(encoding="utf-8") for path in root.rglob("*.py"))
    assert "@title(" not in source
    assert "code_field" not in source
    assert re.search(r"^\s*glossary\s*@=\s*True\s*$", source, re.MULTILINE) is None
    assert "title @=" in source
    assert "test_target_field" in source


def test_vocabulary_references_can_drive_document_titles() -> None:
    source = Path("devdocs/canonical_sources/docs/api/information.py").read_text(
        encoding="utf-8"
    )
    canonical = Path("devdocs/canonical_documents/docs/api/information.md").read_text(
        encoding="utf-8"
    )
    assert 'title @= "{{TERM_13}}"' in source
    assert "## 情報" in canonical
