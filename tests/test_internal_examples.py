from __future__ import annotations

import re
from pathlib import Path

import pytest

from _internal.document_source.examples.architecture import canonical as architecture_source
from _internal.document_source.examples.structured_docs import canonical as structured_docs_source
from _internal.document_source.examples.web_api import canonical as web_api_source
from _internal.document_source.examples.structure_from_body import canonical as structure_from_body_source
from _internal.document_source.vocabulary import canonical as vocabulary_canonical
from shikumi_devdoc.norms.document import Content, Title, VocabularyReference, document
from tests.devdoc_support import document_markdown as markdown


SOURCES = {
    "architecture": architecture_source,
    "structured_docs": structured_docs_source,
    "web_api": web_api_source,
    "structure_from_body": structure_from_body_source,
}


@pytest.mark.parametrize(("name", "source"), SOURCES.items())
def test_example_canonical_readme_is_valid(name: str, source: object) -> None:
    result = document.validate(source, placement=())
    assert result.is_valid, (name, result.diagnostics)
    assert markdown.check(result.view).is_realizable


@pytest.mark.parametrize(("name", "source"), SOURCES.items())
def test_example_canonical_readme_uses_opaque_headings_and_direct_vocabulary_refs(name: str, source: object) -> None:
    view = document.view(source, placement=())
    placeholder_pattern = re.compile(r"\{\{(TERM_[0-9]+)\}\}")

    for item in view.entities:
        assert re.fullmatch(r"TITLE_[0-9]+", item.node.name)
        assert len(item.values(Title)) == 1
        assert len(item.values(Content)) == 1

        referenced_names: list[str] = []
        for text in (*item.values(Title), *item.values(Content)):
            for term_name in placeholder_pattern.findall(text):
                if term_name not in referenced_names:
                    referenced_names.append(term_name)

        references = item.values(VocabularyReference)
        assert [reference.__name__ for reference in references] == referenced_names, name
        assert all(
            reference is getattr(vocabulary_canonical.VOCABULARY, reference.__name__)
            for reference in references
        )


def test_public_example_readmes_are_english_and_structure_example_states_semantic_boundary() -> None:
    root = Path("examples")
    for name in SOURCES:
        readme = root / name / "README.md"
        assert readme.is_file()
        text = readme.read_text(encoding="utf-8")
        assert "{{TERM_" not in text
        assert re.search(r"[ぁ-んァ-ン一-龯]", text) is None

    boundary = (root / "structure_from_body" / "README.md").read_text(encoding="utf-8")
    assert "does **not** by itself verify" in boundary
    assert "semantic accuracy of the translation" in boundary


def test_architecture_example_states_declared_dependency_boundary() -> None:
    canonical_rendered = markdown.realize(document.view(architecture_source, placement=()))
    public = Path("examples/architecture/README.md").read_text(encoding="utf-8")

    assert "`DependsOn`として明示された依存" in canonical_rendered
    assert "実際のPython importやcall graphを自動検出" in canonical_rendered
    assert "dependencies explicitly described through `DependsOn`" in public
    assert "does not discover actual Python imports or call graphs" in public
