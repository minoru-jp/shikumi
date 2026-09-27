# Changelog

Records the major changes in each public release of Shikumi.

## Unreleased

Changes planned for the next public release.

## 0.2.0 - 2026-09-27

Documentation-system restructuring, reusable/logical structure regulations, and the transition to Beta.

### Added

- Added `StructureFragment` / `StructureMount` for reusable partial structure and `LogicalStructureElement` for logical structural roles with unrestricted or enumerated concrete names and cardinality constraints. Explicit `StructureElement`s take precedence over logical elements.
- Added `StructureFragment.unconstrained()` for explicitly regulating a structural element while leaving descendant topology unrestricted.
- Added `StructureElement(required=False)` so an exact named section to be optional while activating its subtree regulation only when that section is present. Optional exact elements still take precedence over `LogicalStructureElement`.
- Extended `LogicalStructureElement` so different logical regulations may coexist below one parent when their fragment root `StructuralKind`s differ, allowing arbitrary-name packages and modules to be resolved without name-pattern dispatch.
- Added `StructureFragment.recursive()` for lazily reapplying the same fragment regulation to recursive children at any observed finite depth.
- Added `StructureGroup` for aggregate cardinality across different exact sibling regulations, including at-least-one and exactly-one layouts.
- Added `StructureCheck.bindings` / `StructureBinding` so structure checking can expose logical-to-actual path bindings without rewriting `ResolvedStructure`.
- Added top-level `STATUS.md` documenting the 0.2.x Beta compatibility policy, criteria for moving to 1.0, and the known documentation-link limitation caused by currently publishing only through PyPI.

### Changed

- Moved the project from Alpha to Beta. Existing exact/actual-path semantics of `StructureElement`, `StructureSpecification.elements`, `element_at()`, `subtree()`, `from_resolved()`, `Focus.placement`, and `ResolvedStructure` are preserved.
- Added Python 3.14 to the supported PyPI classifiers.
- Removed the provisional `.github/workflows/` CI and release workflows while the source repository is not yet public. Verification and PyPI publication are currently performed locally; hosted CI and release automation will be introduced when the repository is published on GitHub.
- Reorganized documentation around shikumi-devdoc 0.3.0: the API Reference is now a collection, semantic contracts live in a separate Specification collection, and executable Descriptor examples are tested from `test_target_field` sources.
- Reduced the README to an entry point and minimal example, reorganized practical documentation as a Guides collection (`Getting Started`, `Defining Descriptors`, and `Project Layout and CLI`), folded the former Distribution Guide into the project-layout guide, and expanded executable documentation tests for examples and CLI commands.
- Moved the repository-only documentation workflow from top-level `DOCUMENTATION_WORKFLOW.md` to `devdocs/README.md`, making it the entry point for the documentation-development workspace.
- Audited executable examples across the API Reference and promoted information attachment, class binding, structure resolution, Semantic View querying, Shikumi composition, validation, structure checking, and realization examples to tested `test_target_field` sources. Signatures and type-shape snippets remain ordinary fenced reference material.
- Reviewed the Specification and API Reference, normalized public subjects to one API node each, and split `shikumi.standard` into its own API page. Corrected API field types, optional arguments, and Specification links; documented Semantic View snapshot reuse, exact structure checking, and default Diagnostic subjects; and added regression coverage for heading and semantic-field structure between canonical and published documents.
- Updated canonical authoring for the revised shikumi-devdoc 0.3.0 surface: nested titles now use `title @= ...` and can resolve Vocabulary references, canonical sources declare their heading policy explicitly, tested snippets use presentation-independent `test_target_field` values with fences owned by prose, and redundant `glossary @= True` declarations were removed because glossary publication is now the default.
- **Breaking:** Moved the official examples out of the top-level `shikumi_examples` import package into reference source under `examples/`, bundled in wheels as `shikumi/_examples/`. Removed their `python -m` execution entry points so user code does not depend on examples as part of the public surface.
- Replaced the four domain-oriented official examples with `examples/structure_showcase`, a domain-light set of valid and invalid package-tree fixtures that demonstrates general structure regulations. Single-feature examples now live as verified code in the Guides and API Reference.

## 0.1.0 - 2026-09-12

Initial public release.

### Added

- Added a Core semantic model that separates Information, Descriptor Use, Structure, and Semantic View.
- Added Validation that handles entities, modules, and packages through the same mechanism, together with Realization through independent Realizers.
- Added reusable Standard Descriptor and Structure implementations for decorators, `@=`, docstrings, and package trees.
- Added a CLI that wires specification bodies, description bodies, and Realizers together through ordinary Python references.
- Added an English public documentation set consisting of the README, Glossary, API Reference, and Distribution Guide. The public documentation is generated and translated from Japanese canonical document sources.
- Added official examples covering architecture validation, structured documentation, Web API DSLs, and `structure-from`.
