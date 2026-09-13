from __future__ import annotations

import re

from _internal.document_source.vocabulary import canonical as vocabulary_canonical
from _internal.document_source.readme import canonical
from tests.devdoc_support import document_markdown as markdown
from shikumi_devdoc.norms.document import (
    CanonicalSource,
    VocabularySource,
    Content,
    VocabularyReference,
    Title,
    document as readme,
)


def test_canonical_readme_description_body_is_valid() -> None:
    result = readme.validate(canonical, placement=())

    assert result.is_valid, result.diagnostics
    assert len(result.view.entities) == 14


def test_readme_heading_names_are_opaque_numeric_identifiers() -> None:
    view = readme.view(canonical, placement=())

    assert all(re.fullmatch(r"TITLE_[0-9]+", item.node.name) for item in view.entities)
    assert all(len(item.values(Title)) == 1 for item in view.entities)
    assert all(len(item.values(Content)) == 1 for item in view.entities)


def test_readme_root_declares_canonical_source_and_vocabulary() -> None:
    view = readme.view(canonical, placement=())
    root = view.item(canonical.TITLE_1)

    assert root.values(VocabularySource) == (vocabulary_canonical,)
    assert root.values(CanonicalSource) == (
        "_internal/document_source/readme/canonical.py",
    )


def test_readme_markdown_realizer_expands_glossary_references() -> None:
    view = readme.view(canonical, placement=())

    check = markdown.check(view)
    assert check.is_realizable, check.diagnostics

    rendered = markdown.realize(view)

    assert rendered.startswith(
        "# Shikumi\n\n"
        "Shikumiは、**構造化ドキュメント生成器、独自DSL、アーキテクチャ検証ツールなどをPython上に構築するためのライブラリ**です。"
    )
    assert "## 実行時確定原則\n" in rendered
    assert "## 検証と実現\n" in rendered
    assert "{{TERM_" not in rendered
    assert "LLMとの迅速な意思疎通" in rendered


def test_readme_mentions_assignment_and_runtime_execution() -> None:
    rendered = markdown.realize(readme.view(canonical, placement=()))

    assert '`title @= "Overview"`は通常の属性代入ではありません。' in rendered
    assert "トップレベルコードは通常のimportと同様に実行されます。" in rendered
    assert "ASTとして読み直しません。" in rendered
    assert "## 警告" in rendered
    assert "信頼できるPythonコードだけにしてください。" in rendered
    assert "検証に使う場合でも、実現に使う場合でも変わりません。" in rendered
    assert "特に検証は、安全な隔離環境で対象を静的に検査する機能ではありません。" in rendered
    assert "通常のimportと同じ権限で任意の処理を実行できます。" in rendered


def test_readme_source_excludes_development_status_material() -> None:
    rendered = markdown.realize(readme.view(canonical, placement=()))

    assert "scratch redesign" not in rendered
    assert "旧 Shikumi" not in rendered
    assert "現在の実装範囲" not in rendered
    assert "まだ契約に含めないもの" not in rendered


def test_readme_states_canonical_document_source_precedence() -> None:
    rendered = markdown.realize(readme.view(canonical, placement=()))

    assert "## 公開文書について" in rendered
    assert "公開文書はすべて英語で提供します。" in rendered
    assert "canonical document sourceを正本" in rendered
    assert "内容に差異がある場合はcanonical document sourceを基準とします。" in rendered


def test_readme_vocabulary_placeholders_have_direct_entity_references() -> None:
    view = readme.view(canonical, placement=())
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


def test_readme_vocabulary_references_do_not_affect_markdown_realization() -> None:
    rendered = markdown.realize(readme.view(canonical, placement=()))

    assert "vocabulary_refs" not in rendered
    assert "TERM_" not in rendered



def test_readme_uses_vocabulary_public_names_for_distribution_imports_and_cli() -> None:
    rendered = markdown.realize(readme.view(canonical, placement=()))

    assert "pip install shikumi" in rendered
    assert "from shikumi import (" in rendered
    assert "from shikumi.standard import assignment, decorator, information_type_rule" in rendered
    assert "validators=[require_title, information_type_rule(Title)]" in rendered
    assert "CLIのentry pointは`shikumi`です。`python -m shikumi`からも同じCLIを実行できます。" in rendered
    assert "shikumi validate \\" in rendered
    assert "shikumi realize \\" in rendered


def test_readme_uses_project_version_from_pyproject_metadata() -> None:
    import tomllib
    from pathlib import Path

    rendered = markdown.realize(readme.view(canonical, placement=()))
    with Path("pyproject.toml").open("rb") as stream:
        project_version = tomllib.load(stream)["project"]["version"]

    assert f"現在のバージョンは `{project_version}` です。" in rendered
    assert "{{PROJECT.version}}" in canonical.TITLE_1.TITLE_3.__doc__

    title = readme.view(canonical, placement=()).item(canonical.TITLE_1.TITLE_3)
    assert [reference.__name__ for reference in title.values(VocabularyReference)] == ["TERM_1"]


def test_readme_states_automatic_inspection_boundaries() -> None:
    rendered = markdown.realize(readme.view(canonical, placement=()))

    assert "## 自動では解析しないもの" in rendered
    assert "実際のimport graphやcall graph" in rendered
    assert "functionやmethodを実体として扱いません" in rendered
