from __future__ import annotations

import re

from _internal.document_source.api_reference import canonical
from tests.devdoc_support import document_markdown as markdown
from shikumi_devdoc.norms.document import (
    Content,
    Title,
    VocabularyReference,
    document,
)
from _internal.document_source.vocabulary import canonical as vocabulary_canonical


def test_canonical_api_reference_description_body_is_valid() -> None:
    result = document.validate(canonical, placement=())

    assert result.is_valid, result.diagnostics
    assert len(result.view.entities) == 88


def test_api_reference_heading_names_are_opaque_numeric_identifiers() -> None:
    view = document.view(canonical, placement=())

    assert all(re.fullmatch(r"TITLE_[0-9]+", item.node.name) for item in view.entities)
    assert all(len(item.values(Title)) == 1 for item in view.entities)
    assert all(len(item.values(Content)) == 1 for item in view.entities)


def test_api_reference_vocabulary_placeholders_have_direct_entity_references() -> None:
    view = document.view(canonical, placement=())
    placeholder_pattern = re.compile(r"\{\{(TERM_[0-9]+)\}\}")

    for item in view.entities:
        referenced_names: list[str] = []
        for text in (*item.values(Title), *item.values(Content)):
            for name in placeholder_pattern.findall(text):
                if name not in referenced_names:
                    referenced_names.append(name)

        references = item.values(VocabularyReference)
        assert [reference.__name__ for reference in references] == referenced_names
        assert all(
            reference is getattr(vocabulary_canonical.VOCABULARY, reference.__name__)
            for reference in references
        )


def test_api_reference_markdown_realization_is_complete() -> None:
    view = document.view(canonical, placement=())
    check = markdown.check(view)

    assert check.is_realizable, check.diagnostics

    rendered = markdown.realize(view)
    assert rendered.startswith("# Shikumi API Reference\n")
    assert "# Core API: `shikumi`" in rendered
    assert "# Standard API: `shikumi.standard`" in rendered
    assert "# CLI: `shikumi`" in rendered
    assert "{{TERM_" not in rendered


def test_api_reference_states_python_structure_entity_scope_and_exact_specification() -> None:
    rendered = markdown.realize(document.view(canonical, placement=()))

    assert "functionやmethodは実体に含めない" in rendered
    assert "現在の構造照合は完全一致" in rendered
    assert "規定にない追加要素もerror" in rendered
