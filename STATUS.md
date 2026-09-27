# Shikumi Project Status

This document describes Shikumi's current development stage, compatibility policy, and criteria for moving toward 1.0.

Shikumi enters **Beta** with version 0.2.0. Beta does not mean that the public API is open to unrestricted change. The current core design and public API are considered mature enough for real-world use, and compatibility will be actively preserved from this point forward.

## Current status

The current public release series is `0.2.x`, with development status **Beta**.

Version 0.2.0 establishes the foundation to be exercised in real projects, including the reorganized documentation system and the expanded Structure regulation API. The Beta period is not intended for redesigning the API from scratch. It is a period for validating the current design through dependent projects and real use while making necessary improvements without unnecessary breakage.

## Stability policy

From 0.2.0 onward, breaking changes to the public API will not be made without a significant reason.

Significant reasons include defects where preserving the existing behavior would compromise correctness, safety, or the integrity of the core design. Normal feature development and improvements should be additive. When an existing public API must eventually be replaced, Shikumi will use deprecation and a migration period whenever practical.

Internal implementation details, documentation-generation infrastructure, and private development structures are outside this compatibility policy, but preserving published semantic contracts remains the priority.

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

## Distribution note

Shikumi is currently published **only through PyPI**. There is not yet a public web page for browsing the source repository.

As a result, some repository-relative links in the README and other published documentation do not resolve when the documentation is viewed on PyPI. This is a known limitation of the current distribution setup.

When the source repository is published on the web, for example on GitHub, the documentation links will be revised against the public repository URL so that they resolve correctly from the published documentation.

There is also no hosted CI at present because there is no public source repository yet. Release verification and PyPI uploads are currently performed locally. CI will be introduced when the repository is published on GitHub and can be configured against that public environment.
