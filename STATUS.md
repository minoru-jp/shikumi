# Shikumi Project Status

This document describes Shikumi's current development stage, compatibility policy, and criteria for moving toward 1.0.

Shikumi enters **Beta** with version 0.2.0. Beta does not mean that the public API is open to unrestricted change. The current core design and public API are considered mature enough for real-world use, and compatibility will be actively preserved from this point forward.

## Current status

The current public release is `0.2.4`, in the `0.2.x` release series, with development status **Beta**.

Version 0.2.0 establishes the foundation to be exercised in real projects, including the reorganized documentation system and the expanded Structure regulation API. The Beta period is not intended for redesigning the API from scratch. It is a period for validating the current design through dependent projects and real use while making necessary improvements without unnecessary breakage.

## Stability policy

From 0.2.0 onward, breaking changes to the public API will not be made without a significant reason.

Significant reasons include defects where preserving the existing behavior would compromise correctness, safety, or the integrity of the core design. Normal feature development and improvements should be additive. When an existing public API must eventually be replaced, Shikumi will use deprecation and a migration period whenever practical.

Internal implementation details, documentation-generation infrastructure, and private development structures are outside this compatibility policy, but preserving published semantic contracts remains the priority.

## Public typing contract

Shikumi distributes `py.typed` and verifies both a clean basedpyright result for the package source and a consumer-side typing contract under `tests/typing`. In 0.2.4, that consumer contract covers repeated custom `@=` descriptions built with `class_binding()` in addition to the standard Descriptors.

`class_binding()` returns `ClassBinding[T]`, preserving the first value type `T` across later `@=` writes under the same binding name. `ClassBinding[T]` is a public static typing contract; the concrete temporary binding implementation used inside a class body remains an internal detail.

The low-level `class_binding()` API exposes its temporary runtime binding as `ClassBinding[T]`. By contrast, `shikumi.standard.assignment()` is a higher-level standard Descriptor and intentionally keeps the writer's own static type visible across augmented assignment, treating the temporary binding as an implementation detail. These contracts differ by abstraction level; `@=` itself is not a syntax required by Shikumi Core.

The public lifecycle contract of `class_binding()` is that the callback is applied after class-body execution and before `__init_subclass__()`. The current implementation uses `__set_name__()` to realize that timing, but that specific hook is not itself part of the public contract. Shikumi also does not normalize callback exceptions, so the externally visible exception shape follows Python's class-creation semantics and differs between Python 3.11 and Python 3.12 or later.

## Beta goals

During the Beta period, the project will particularly verify that:

- the current semantic model and public API remain practical for continued use in real projects built on Shikumi;
- dependent projects, including `shikumi-devdoc`, can evolve without breaking compatibility;
- the major contracts around Structure, Validation, Realization, and Descriptors do not require fundamental redesign;
- new APIs can be added without collapsing the existing conceptual boundaries; and
- documentation, diagnostics, typing, and other usability aspects can continue to improve without destabilizing the foundation.

## Path to 1.0

After sufficient real-world use, Shikumi will move to `1.0.0` when there are no known fundamental design problems and no expected need for a breaking redesign of the current foundation.

The criterion for 1.0 is not an unlimited accumulation of features. The important condition is confidence that the current public API and conceptual model can continue to serve as a stable foundation for dependent projects.

## Distribution and repository operations

Shikumi is published through PyPI and the public GitHub repository `https://github.com/minoru-jp/shikumi`. PyPI is the distribution channel for the Python package, while GitHub is the public home for the source, published documentation, issues, and development history.

The top-level README uses absolute URLs in the public GitHub repository for its main documentation, official example, and LICENSE links, so the same published documents can be reached both from GitHub and when the README is rendered on PyPI. Package metadata also publishes Homepage, Repository, Documentation, and Issues URLs.

Hosted CI runs on GitHub Actions for pushes and pull requests to `main`. Its quality job runs quality checks with Ruff and basedpyright, requiring clean Ruff lint and formatting plus zero basedpyright errors or warnings for the package source. It also runs the dedicated basedpyright consumer typing contract under `tests/typing`, which fixes the intended accept/reject behavior of the public typed API. CI also tests Python 3.11 through 3.14, checks canonical-document drift, builds the wheel and sdist, and verifies the distribution contents.

PyPI publication is separated from ordinary pushes. `.github/workflows/release.yml` runs only when a GitHub Release is published and re-runs the same reusable checks as ordinary CI against the release-tag commit: Ruff, package-source basedpyright, the consumer typing contract, canonical-document drift, and the Python 3.11 through 3.14 test suite. Only after those checks succeed and the release tag matches the version in `pyproject.toml` does it build the distributions and publish them with PyPI Trusted Publishing. The GitHub `pypi` environment and the corresponding Trusted Publisher on PyPI are configured and linked.
