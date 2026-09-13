from __future__ import annotations

import re

from _internal.document_source import changelog as changelog_source
from _internal.document_source.changelog import canonical, released
from _internal.document_source.vocabulary import canonical as vocabulary_canonical
from shikumi_devdoc.norms.changelog import (
    ChangeContent,
    ChangeKindInformation,
    ChangelogTitle,
    ReleaseDate,
    ReleaseLabel,
    changelog_system,
)
from shikumi_devdoc.norms.document import VocabularyReference
from tests.devdoc_support import changelog_markdown as markdown


def test_canonical_changelog_description_body_is_valid() -> None:
    result = changelog_system.validate(changelog_source, placement=())

    assert result.is_valid, result.diagnostics
    assert len(result.view.entities) == 11


def test_changelog_uses_fixed_three_level_entity_shapes() -> None:
    view = changelog_system.view(changelog_source, placement=())
    root = view.item(canonical.CHANGELOG)

    assert root.values(ChangelogTitle) == ("Changelog",)
    releases = [item for item in view.entities if item.subject is released.CHANGELOG_PART.RELEASE_1]
    assert len(releases) == 1
    assert re.fullmatch(r"RELEASE_[0-9]+", releases[0].node.name)
    assert releases[0].values(ReleaseLabel) == ("0.1.0",)
    assert releases[0].values(ReleaseDate) == ("2026-09-12",)

    changes = [item for item in view.entities if item.node.parent is releases[0].subject]
    assert len(changes) == 6
    assert all(re.fullmatch(r"CHANGE_[0-9]+", item.node.name) for item in changes)
    assert all(len(item.values(ChangeKindInformation)) == 1 for item in changes)
    assert all(len(item.values(ChangeContent)) == 1 for item in changes)
    assert not any(item.node.parent in {change.subject for change in changes} for item in view.entities)


def test_changelog_markdown_realizer_groups_changes_without_extra_python_ids() -> None:
    view = changelog_system.view(changelog_source, placement=())
    check = markdown.check(view)

    assert check.is_realizable, check.diagnostics
    rendered = markdown.realize(view)

    assert rendered.startswith("# Changelog\n\nShikumiの公開リリースごとの主な変更を記録します。")
    assert "## Unreleased" in rendered
    assert "**Breaking:**" in rendered
    assert "## 0.1.0 - 2026-09-12" in rendered
    assert "### Added" in rendered
    assert "RELEASE_" not in rendered
    assert "CHANGE_" not in rendered
    assert "vocabulary_refs" not in rendered
    assert "{{TERM_" not in rendered


def test_changelog_vocabulary_placeholders_have_direct_entity_references() -> None:
    view = changelog_system.view(changelog_source, placement=())
    placeholder_pattern = re.compile(r"\{\{(TERM_[0-9]+)\}\}")

    for item in view.entities:
        referenced_names: list[str] = []
        for information_type in (ChangelogTitle, ReleaseLabel, ChangeContent):
            for text in item.values(information_type):
                for name in placeholder_pattern.findall(text):
                    if name not in referenced_names:
                        referenced_names.append(name)

        # Root introduction is intentionally checked separately because it has
        # a dedicated changelog information type rather than ChangeContent.
        if item.subject is canonical.CHANGELOG:
            from shikumi_devdoc.norms.changelog import Introduction

            for text in item.values(Introduction):
                for name in placeholder_pattern.findall(text):
                    if name not in referenced_names:
                        referenced_names.append(name)

        references = item.values(VocabularyReference)
        assert [reference.__name__ for reference in references] == referenced_names
        assert all(
            reference is getattr(vocabulary_canonical.VOCABULARY, reference.__name__)
            for reference in references
        )


def test_released_changelog_entries_are_kept_in_a_partition() -> None:
    from shikumi_devdoc.norms.changelog import ChangelogPartOrder

    view = changelog_system.view(changelog_source, placement=())
    part = view.item(released.CHANGELOG_PART)
    assert part.values(ChangelogPartOrder) == (10,)
    assert not any(item.node.parent is canonical.CHANGELOG for item in view.entities if item.has(ReleaseLabel))
