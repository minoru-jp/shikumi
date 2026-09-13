# Documentation Workflow

This repository manages public and repository-only documentation from canonical document sources under `_internal/document_source/`.

Placed Markdown is not the source of truth. Documentation changes flow in one direction from the canonical source through validation and realization by `shikumi-devdoc`, translation, and placement.

## Dependency relationship

`shikumi-devdoc` is a development-time tool used to generate documentation for this repository. It is not a runtime dependency of the `shikumi` package.

At the package level, `shikumi-devdoc` uses `shikumi`. At the repository-maintenance level, this repository uses `shikumi-devdoc` and ships the generated Markdown artifacts. For that reason, `shikumi-devdoc` belongs in a development dependency group, not in `[project.dependencies]`.

During documentation generation, the checked-out `src/shikumi` is importable so that `shikumi-devdoc` interprets the version of Shikumi currently being developed.

## Sources of truth and generated artifacts

Documentation content is authoritative in `_internal/document_source/**/canonical.py`. The generated `_internal/document_source/vocabulary/terms.py` module is an IDE-facing reference artifact, not a source of truth.

Japanese Markdown under `_internal/document_build/ja/` is a **committed intermediate document** realized from the canonical sources by `shikumi-devdoc`. It is committed so realization changes can be reviewed, but it must not be edited directly.

English Markdown is the translated public or repository-only placement of those intermediate documents. If the canonical source, intermediate document, and English placement disagree, the canonical document source takes precedence.

The Python implementation described by a document is outside this rule. The implementation remains authoritative in its normal package or module.

## Basic flow

```text
canonical.py
    ↓ shikumi-devdoc validation / realization
_internal/document_build/ja/ Japanese Markdown
    ↓ translation
English Markdown
    ↓ placement
repository / distribution
```

1. Create or update the canonical document source.
2. Run `python scripts/render_canonical_docs.py` to regenerate the Vocabulary term-reference module and Japanese intermediate documents.
3. Review the intermediate-document diff.
4. Translate the intermediate document into English.
5. Place the translation at the repository location defined for that document.
6. Run `python scripts/render_canonical_docs.py --check`, relevant tests, and checks for links, public names, and distribution placement.

## Intermediate documents

The files under `_internal/document_build/ja/` are translation inputs and reviewable realization artifacts.

- Commit them to the repository.
- Do not include them in wheels or sdists.
- Do not edit them as documentation sources of truth.
- If a change is needed, update the canonical source and regenerate them.
- Generation embeds the repository notice and translation metadata used by the translation step.

This makes canonical-source changes, realization changes, and English-translation changes independently reviewable.

## External context

Project name, version, `requires-python`, public import package name, CLI entry point, and distribution name already have authoritative values in `pyproject.toml`. They are not duplicated as fixed values in canonical document sources.

`scripts/render_canonical_docs.py` constructs the `shikumi-devdoc` context from current project metadata and supplies values for context references such as `PROJECT.version` during realization.

## Updating an existing document

Do not begin an update by editing either placed English Markdown or a committed intermediate document.

1. Change the corresponding `canonical.py`.
2. Regenerate intermediates, including `terms.py` when the Vocabulary changed.
3. Review the Japanese intermediate diff.
4. Translate the intermediate document into English.
5. Replace the existing English placement with the translation.
6. Verify generated-artifact consistency and run relevant tests.

If a problem is discovered only in the English version, reflect the final fix in the canonical source and regenerate from there.

## Adding a new document

First decide whether the document can reuse the document, Vocabulary, or CHANGELOG regulations provided by `shikumi-devdoc`.

For every new document, decide at least:

- canonical source location
- `shikumi-devdoc` regulation and Realizer to use
- intermediate location under `_internal/document_build/ja/`
- English placement
- validation tests for the canonical source
- whether the document is repository-only or also belongs in the wheel / sdist

Add new generated artifacts to `scripts/render_canonical_docs.py`. Update `pyproject.toml` and distribution archive checks only for documents that ship in distributions.

## Translation

Placed documentation is provided in English. Translation must preserve the meaning, section structure, code examples, public API names, Python names, CLI names, paths, and other literal identifiers present in the intermediate document.

Terms identified for spelling preservation by the `shikumi-devdoc` translation-source metadata must keep their spelling. The generated notice and translation-metadata comments at the start of intermediate files must not be copied into public documents.

Do not add specifications or explanations absent from the intermediate document. If the source is ambiguous or incomplete, update the canonical source and restart from intermediate generation.

## Placement and distribution

README, public references, official example READMEs, and CHANGELOG may be shipped in distributions. Maintenance-only documentation may remain repository-only.

`_internal/document_source/`, `_internal/document_build/`, and `shikumi-devdoc` itself are not included in Shikumi wheels or sdists.

`DOCUMENTATION_WORKFLOW.md` is repository-only and must not be included in wheels or sdists.

## Verification

After placing documentation, verify at least that:

- each canonical source satisfies its regulation
- `python scripts/render_canonical_docs.py --check` succeeds, proving committed `terms.py` and Japanese intermediates can be reproduced from the canonical sources
- no unresolved Vocabulary or context placeholders remain in intermediate documents
- code examples, links, and public names in English placements remain valid
- archive checks agree with the intended placement of distribution documents

CI also checks for generated-document drift.
