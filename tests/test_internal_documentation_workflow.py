from __future__ import annotations

import re
from pathlib import Path

from _internal.document_source.documentation_workflow import canonical
from _internal.document_source.vocabulary import canonical as vocabulary_canonical
from shikumi_devdoc.norms.document import (
    Content,
    Title,
    VocabularyReference,
    document,
)
from tests.devdoc_support import document_markdown as markdown


def test_documentation_workflow_source_is_valid() -> None:
    result = document.validate(canonical, placement=())

    assert result.is_valid, result.diagnostics
    assert len(result.view.entities) == 11


def test_documentation_workflow_is_realizable() -> None:
    view = document.view(canonical, placement=())
    check = markdown.check(view)

    assert check.is_realizable, check.diagnostics
    rendered = markdown.realize(view)
    assert rendered.startswith("# 文書運用\n")
    assert "## 基本フロー\n" in rendered
    assert "_internal/document_build/ja/ の日本語 Markdown" in rendered
    assert "shikumi-devdoc" in rendered
    assert "DOCUMENTATION_WORKFLOW.md` 自身はリポジトリ専用文書" in rendered
    assert "{{TERM_" not in rendered


def test_documentation_workflow_heading_names_are_opaque_numeric_identifiers() -> None:
    view = document.view(canonical, placement=())

    assert all(re.fullmatch(r"TITLE_[0-9]+", item.node.name) for item in view.entities)
    assert all(len(item.values(Title)) == 1 for item in view.entities)
    assert all(len(item.values(Content)) == 1 for item in view.entities)


def test_documentation_workflow_vocabulary_placeholders_have_direct_refs() -> None:
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


def test_repository_documentation_workflow_is_english_and_repository_only() -> None:
    path = Path("DOCUMENTATION_WORKFLOW.md")
    assert path.is_file()

    text = path.read_text(encoding="utf-8")
    assert text.startswith("# Documentation Workflow\n")
    assert "canonical.py" in text
    assert "Intermediate documents" in text
    assert "must not be included in wheels or sdists" in text
    assert re.search(r"[ぁ-んァ-ヶ一-龯]", text) is None

    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    assert "DOCUMENTATION_WORKFLOW.md" not in pyproject
