from __future__ import annotations

import re

from _internal.document_source.distribution_guide import canonical
from _internal.document_source.vocabulary import canonical as vocabulary_canonical
from shikumi_devdoc.norms.document import (
    Content,
    Title,
    VocabularyReference,
    document,
)
from tests.devdoc_support import document_markdown as markdown


def test_canonical_distribution_guide_description_body_is_valid() -> None:
    result = document.validate(canonical, placement=())

    assert result.is_valid, result.diagnostics
    assert len(result.view.entities) == 5


def test_distribution_guide_heading_names_are_opaque_numeric_identifiers() -> None:
    view = document.view(canonical, placement=())

    assert all(re.fullmatch(r"TITLE_[0-9]+", item.node.name) for item in view.entities)
    assert all(len(item.values(Title)) == 1 for item in view.entities)
    assert all(len(item.values(Content)) == 1 for item in view.entities)


def test_distribution_guide_vocabulary_placeholders_have_direct_entity_references() -> None:
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


def test_distribution_guide_markdown_realization_is_complete() -> None:
    view = document.view(canonical, placement=())
    check = markdown.check(view)

    assert check.is_realizable, check.diagnostics
    rendered = markdown.realize(view)
    assert rendered.startswith("# 規定体・記述体・実現器の配置\n")
    assert "## 目的" in rendered
    assert "## 推奨配置" in rendered
    assert "## CLI から参照する" in rendered
    assert "## 配置と配布の自由" in rendered
    assert "{{TERM_" not in rendered


def test_distribution_guide_starts_from_cli_goal_and_recommends_clear_layout() -> None:
    rendered = markdown.realize(document.view(canonical, placement=()))

    assert "最終的に CLI から通常の Python import で参照できる形" in rendered
    assert "shikumi_lib/" in rendered
    assert "norms/" in rendered
    assert "realizers/" in rendered
    assert "CLI から参照できることが確認できれば、配置上の目的は達成されている。" in rendered
    assert "推奨作例であり、Shikumi の要求ではない" in rendered
    assert "独立して作成したコードには作者が任意のライセンスを設定できる" in rendered
    assert "取り込んだ第三者コードにはそのライセンスが適用される" in rendered


def test_distribution_guide_states_examples_are_intentionally_bundled() -> None:
    rendered = markdown.realize(document.view(canonical, placement=()))

    assert "公式作例は" in rendered
    assert "参考ソースとして本体distributionに同梱" in rendered
    assert "公開import packageやCLI entry pointではない" in rendered
    assert "repositoryでは`examples/`、wheelでは`shikumi/_examples/`" in rendered
