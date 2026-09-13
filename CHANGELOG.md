# Changelog

Records the major changes in each public release of Shikumi.

## Unreleased

Changes planned for the next public release.

### Changed

- **Breaking:** Moved the official examples out of the top-level `shikumi_examples` import package into reference source under `examples/`, bundled in wheels as `shikumi/_examples/`. Removed their `python -m` execution entry points so user code does not depend on examples as part of the public surface.

## 0.1.0 - 2026-09-12

Initial public release.

### Added

- Added a Core semantic model that separates Information, Descriptor Use, Structure, and Semantic View.
- Added Validation that handles entities, modules, and packages through the same mechanism, together with Realization through independent Realizers.
- Added reusable Standard Descriptor and Structure implementations for decorators, `@=`, docstrings, and package trees.
- Added a CLI that wires specification bodies, description bodies, and Realizers together through ordinary Python references.
- Added an English public documentation set consisting of the README, Glossary, API Reference, and Distribution Guide. The public documentation is generated and translated from Japanese canonical document sources.
- Added official examples covering architecture validation, structured documentation, Web API DSLs, and `structure-from`.
