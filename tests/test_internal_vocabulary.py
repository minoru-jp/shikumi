from __future__ import annotations

import re

from tests.devdoc_support import glossary_markdown as markdown
from _internal.document_source.vocabulary import canonical
from shikumi_devdoc.norms.vocabulary import (
    Definition,
    Glossary,
    Introduction,
    TermName,
    Title,
    PreserveSpelling,
    vocabulary_system,
)


def test_canonical_vocabulary_description_body_is_valid() -> None:
    result = vocabulary_system.validate(canonical, placement=())

    assert result.is_valid, result.diagnostics

    documents = [item for item in result.view.entities if item.has(Title)]
    entries = [item for item in result.view.entities if item.has(TermName)]
    assert len(documents) == 1
    assert len(entries) == 32


def test_vocabulary_root_carries_glossary_title_and_introduction() -> None:
    view = vocabulary_system.view(canonical, placement=())
    document = view.item(canonical.VOCABULARY)

    assert document.values(Title) == ("Shikumi 用語集",)
    assert document.values(Introduction) == (
        "Shikumi における正規の用語と、その意味上の境界を定義する。",
    )


def test_canonical_vocabulary_entry_names_are_opaque_numeric_identifiers() -> None:
    view = vocabulary_system.view(canonical, placement=())
    entries = [item for item in view.entities if item.has(TermName)]

    assert all(re.fullmatch(r"TERM_[0-9]+", item.node.name) for item in entries)
    assert all(item.node.parent is canonical.VOCABULARY for item in entries)


def test_shikumi_term_is_marked_preserve_spelling_and_public_in_glossary() -> None:
    view = vocabulary_system.view(canonical, placement=())
    shikumi = view.item(canonical.VOCABULARY.TERM_1)

    assert shikumi.values(TermName) == ("Shikumi",)
    assert shikumi.values(PreserveSpelling) == (True,)
    assert shikumi.values(Glossary) == (True,)
    assert shikumi.values(Definition) == (
        "Python 上の対象を、構造と情報に基づく一つの意味体系として解釈する構成単位。\n\n"
        "Shikumi は、解釈対象から意味像を構成し、その意味像を検証や実現から利用できる形で提供する。",
    )


def test_public_names_are_supplied_by_external_context_instead_of_duplicate_terms() -> None:
    assert not hasattr(canonical.VOCABULARY, "TERM_30")
    assert not hasattr(canonical.VOCABULARY, "TERM_31")
    assert not hasattr(canonical.VOCABULARY, "TERM_32")

def test_markdown_glossary_realizer_emits_only_entries_marked_for_glossary() -> None:
    view = vocabulary_system.view(canonical, placement=())

    check = markdown.check(view)
    assert check.is_realizable, check.diagnostics

    rendered = markdown.realize(view)

    assert rendered.startswith(
        "# Shikumi 用語集\n\n"
        "Shikumi における正規の用語と、その意味上の境界を定義する。\n\n"
        "## Shikumi\n\n"
        "Python 上の対象を、構造と情報に基づく一つの意味体系として解釈する構成単位。"
    )
    assert "## 実行時確定原則\n" in rendered
    assert "Python コードから Shikumi の公開 API" not in rendered
    assert "コマンドラインから Shikumi CLI" not in rendered
    assert "Python packageを配布・インストール" not in rendered
    assert "TERM_" not in rendered
    assert "untranslatable" not in rendered
    assert "glossary" not in rendered
    assert "True" not in rendered
    assert rendered.count("\n## ") == 29


def test_recommended_project_local_shikumi_layout_names_are_vocabulary_only() -> None:
    view = vocabulary_system.view(canonical, placement=())

    shikumi_lib = view.item(canonical.VOCABULARY.TERM_33)
    norms = view.item(canonical.VOCABULARY.TERM_34)
    realizers = view.item(canonical.VOCABULARY.TERM_35)

    assert shikumi_lib.values(TermName) == ("shikumi_lib",)
    assert norms.values(TermName) == ("norms",)
    assert realizers.values(TermName) == ("realizers",)
    assert shikumi_lib.values(PreserveSpelling) == (True,)
    assert norms.values(PreserveSpelling) == (True,)
    assert realizers.values(PreserveSpelling) == (True,)
    assert shikumi_lib.values(Glossary) == ()
    assert norms.values(Glossary) == ()
    assert realizers.values(Glossary) == ()


def test_generated_term_reference_module_preserves_canonical_identity() -> None:
    from _internal.document_source.vocabulary import terms

    assert terms.__shikumi_devdoc_vocabulary_source__ is canonical
    assert terms.TERM_1.__shikumi_devdoc_vocabulary_target__ is canonical.VOCABULARY.TERM_1
    assert terms.TERM_33.__shikumi_devdoc_vocabulary_target__ is canonical.VOCABULARY.TERM_33
