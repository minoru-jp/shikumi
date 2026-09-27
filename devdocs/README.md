# devdocs

This repository generates public and repository-only documentation from canonical sources under `devdocs/`.

Placed Markdown is not the source of truth. Documentation changes flow in one direction from the canonical source through validation and realization by `shikumi-devdoc`, review of the canonical document, translation, and placement.

## Dependency relationship

`shikumi-devdoc` is a development-time tool used to generate documentation for this repository. It is not a runtime dependency of the `shikumi` package.

At the package level, `shikumi-devdoc` uses `shikumi`. At the repository-maintenance level, this repository uses `shikumi-devdoc`. Therefore `shikumi-devdoc` is pinned in `[dependency-groups].docs` and is not added to `[project.dependencies]`.

During documentation generation, the checked-out `src/shikumi` is importable so `shikumi-devdoc` interprets the version of Shikumi currently being developed.

## Three documentation boundaries

The source of truth for documentation content is the Python **canonical source** under `devdocs/canonical_sources/`.

Japanese Markdown under `devdocs/canonical_documents/` is the **canonical document** realized from the canonical source and realization context. It is committed so generated changes can be reviewed, but it must not be edited directly.

English Markdown placed at the repository root, under `docs/`, in `examples/*/README.md`, or in this `devdocs/README.md` is the **published document** translated and placed from the canonical document.

If the canonical source, canonical document, and published document differ, the canonical source takes precedence for documentation content. The Python implementation described by a document remains authoritative in its normal package or module.

## Workspace

`devdocs/` separates these responsibilities:

- `README.md`: entry point and operating rules for this documentation-development workspace.
- `canonical_sources/`: Python sources that are authoritative for documentation content.
- `canonical_documents/`: committed Japanese canonical documents.
- `config/`: fixed inputs explicitly supplied during realization, currently including the generated-document notice.

Vocabulary reference modules are not generated. Documents merge canonical Vocabulary term classes directly. Glossary publication is the default; use `glossary @= False` only for terms that should be excluded from the public glossary.

## Document responsibilities

Repository documents are separated by responsibility:

- `README.md`: project entry point, use cases, minimal example, and primary navigation.
- `docs/glossary.md`: canonical terminology and conceptual boundaries.
- `docs/api/`: reference collection for the current public Python API and CLI surface.
- `docs/specification/`: independently referenceable semantic and compatibility contracts.
- `docs/guides/`: a guide collection for Getting Started, Descriptor authoring, project layout, and CLI wiring.
- `examples/`: executable valid/invalid fixtures that showcase general structural regulations.
- `CHANGELOG.md`: release-centered history.
- `devdocs/README.md`: documentation authoring and generation workflow for repository maintainers.

Do not mix design contracts or long tutorials into the API Reference. Put contracts in the Specification, practical procedures in Guides, and canonical concept definitions in the Glossary. Keep the README focused on the project entry point and minimal example rather than turning it into a second guide set.

## Basic flow

After changing a canonical source, regenerate the canonical documents:

```bash
python scripts/render_canonical_docs.py
```

Review the generated Japanese documents, translate and place the corresponding English published documents, then verify drift:

```bash
python scripts/render_canonical_docs.py --check
```

The normal sequence is:

1. Create or update the canonical source.
2. Regenerate canonical documents.
3. Review the Japanese canonical-document diff.
4. Translate the canonical document into English.
5. Place the translation at the published-document location.
6. Test documentation drift, documented code, links, public names, and distribution placement.

## Realization context

Values already authoritative in `pyproject.toml`, such as project name, version, `requires-python`, public import package, CLI entry point, and distribution name, are not duplicated as fixed text in canonical sources.

`scripts/render_canonical_docs.py` builds the realization context from `pyproject.toml`. Fixed generation instructions are supplied explicitly from `devdocs/config/notice.toml`.

## Code in documentation

Code, commands, configuration, or expected output whose literal value is worth checking directly from ordinary tests is separated from prose with `test_target_field` and covered by a corresponding test.

Public API examples, imports, descriptor definitions, validation examples, and realization examples should normally be tested. Short expressions, pseudocode, and structural diagrams do not need to become `test_target_field` values merely because they are fenced code blocks.

`test_target_field` does not own Markdown presentation. Put the fenced block and its language in the surrounding docstring or prose template, and keep only the literal test target in the field. API signatures, dataclass shapes, enum values, and similar reference-only fences may remain directly in prose.

When intentionally invalid code is documented and the failure itself is contractual, the failure should also be tested.

## Adding a document

Start by deciding the audience and responsibility of the document. Split a collection because responsibilities, reference targets, or reader goals are independently meaningful, not merely because a file is long.

Canonical sources use the generic document model. Structured information should become fields only when the structure has a concrete purpose. Nested human-readable titles use `title @= ...`; when useful, titles may resolve Vocabulary references through the node-local `merge` namespace.

Every document declares its nested heading policy explicitly with `heading="title"` or `heading="identity"` on `@canonical_source(...)`. Narrative, API, and guide documents use title headings; Specification pages use identity headings because their nested rule nodes are stable semantic-reference targets.

API Reference, Specification, CHANGELOG, and similar documents may reuse standard field sets from `shikumi_devdoc.fields` where appropriate. For a collection, keep each page as an independent canonical document, provide `@summary(...)` and an `order` only where useful, and realize `INDEX.md` separately with `render index`.

## Translation and publication

Published documents are provided in English. Translation preserves meaning, section structure, semantic fields, code examples, public API names, Python names, CLI names, and paths from the canonical document. In the API Reference and Specification, translation must not rearrange heading hierarchy or field placement for stylistic reasons.

Terms marked for `preserve_spelling` in translation-source metadata keep their spelling. The generated notice and translation metadata at the beginning of a canonical document are not included in the published document.

If translation exposes ambiguity or missing specification, fix the canonical source and regenerate rather than patching only the published document.

## Placement and distribution

The wheel is the distribution for using Shikumi and contains the implementation, public documentation, and official examples. Repository sources used to develop or verify a release, such as `tests/`, `devdocs/`, and `scripts/`, are not included in the wheel.

The sdist is the complete release source from which that release can be reconstructed, verified, and understood. In addition to `src/`, public documentation, and `examples/`, it includes `tests/`, `devdocs/`, `scripts/`, and project metadata. Repository-operation settings such as `.github/`, VCS metadata, virtual environments, caches, build outputs, and other material that is not release source are excluded.

The canonical sources and canonical documents under `devdocs/` are included in the sdist, but they are not public Python API.

## Verification

For documentation changes, verify at least that:

- every canonical source satisfies the applicable `shikumi-devdoc` regulation;
- `python scripts/render_canonical_docs.py --check` succeeds and reproduces committed canonical documents;
- canonical documents contain no unresolved Vocabulary or context placeholders;
- tests for values published through `test_target_field` succeed;
- published API Reference and Specification documents preserve the canonical heading hierarchy and semantic-field structure;
- published code examples, links, and public names remain valid; and
- packaging tests match the intended placement of distributed documents.

There is no hosted CI yet, so these checks are currently run locally. CI will be introduced when the repository is published on GitHub, including automated checks for canonical-document drift and documented code examples.
