# Shikumi

Shikumi is a library for **building Python systems with application-defined meaning, structure, and rules**.

It does not directly provide a structured-document generator, a domain-specific language, or an architecture validator. Instead, it provides the common foundation for composing those systems from Information Types, Descriptors, Structure, Validators, and Realizers defined by the application.

Shikumi interprets Python objects after execution and constructs a Semantic View. The same Semantic View can be used for both Validation and Realization.

## Typical uses

- Generate artifacts such as Markdown, configuration, or reports from descriptions written in Python.
- Build Python-based DSLs with application-specific attributes, classifications, and relationships.
- Define and validate package, module, class, or dependency structures.
- Apply the same regulation to multiple Python packages.
- Use machine-readable descriptions with explicit meaning and structure in LLM-assisted workflows.

These application-specific semantics are not built into Shikumi. They are defined by the user as a regulation for the intended use case.

## Installation

```bash
pip install shikumi
```

Current version: `0.2.2`. Shikumi requires Python `>=3.11`. Development status is Beta from 0.2.0.

## Minimal example

This example defines a `title` Information Type, describes the same semantic information through both `@=` and a decorator, and applies a Validator requiring entities to have a title.

```python
from shikumi import (
    DescriptorUseRule,
    Diagnostic,
    InformationType,
    Shikumi,
    StructuralKind,
    StructureSelector,
    validator,
)
from shikumi.standard import assignment, decorator, information_type_rule

Title = InformationType("title", str)
title = assignment(Title)
titled = decorator(Title)


class Overview:
    title @= "Overview"


@titled("Tutorial")
class Tutorial:
    pass


@validator(focus=StructuralKind.ENTITY)
def require_title(view):
    if not view.focused.has(Title):
        yield Diagnostic("title is required")


docs = Shikumi(
    information_types=[Title],
    validators=[require_title, information_type_rule(Title)],
    descriptor_rules=[
        DescriptorUseRule(
            descriptor=title,
            allowed=StructureSelector(kind=StructuralKind.ENTITY),
            name="title",
        )
    ],
)

assert docs.view(Overview).focused.values(Title) == ("Overview",)
assert docs.validate(Overview).is_valid
```

`InformationType` defines what a value means. Descriptors define how that meaning is written in Python. `view()` constructs a Semantic View, while `validate()` applies Validators to that view.

For an end-to-end example that continues through Realization, see [Getting Started](https://github.com/minoru-jp/shikumi/blob/main/docs/guides/getting-started.md).

## Runtime model and safety

Shikumi is not a static analyzer that reconstructs meaning from Python source or ASTs. When a module or package is used as input, it is imported as ordinary Python code. Shikumi then interprets the runtime objects, Information, and Descriptor Uses that exist after execution.

**Only give Shikumi modules and packages that contain trusted Python code.** Import-time code executes with the normal privileges of the current process even when the purpose is Validation.

The exact contracts for runtime determination, Structure, Validation, and Realization are documented in the [Specification](https://github.com/minoru-jp/shikumi/blob/main/docs/specification/INDEX.md).

## Official example

[`structure_showcase`](https://github.com/minoru-jp/shikumi/blob/main/examples/structure_showcase/README.md) is an executable, domain-light showcase of general structural patterns expressible with `StructureSpecification`.

Single-feature usage belongs in the verified code examples in the Guides and API Reference. The `examples/` directory is reserved for a composed structural showcase with valid and invalid fixtures.

## Documentation

- [Guides](https://github.com/minoru-jp/shikumi/blob/main/docs/guides/INDEX.md): getting started, Descriptor authoring, project layout, and CLI wiring.
- [Glossary](https://github.com/minoru-jp/shikumi/blob/main/docs/glossary.md): canonical definitions of Shikumi terminology.
- [API Reference](https://github.com/minoru-jp/shikumi/blob/main/docs/api/INDEX.md): public Python API and CLI surface.
- [Specification](https://github.com/minoru-jp/shikumi/blob/main/docs/specification/INDEX.md): semantic and compatibility contracts guaranteed by Shikumi.
- [STATUS](https://github.com/minoru-jp/shikumi/blob/main/STATUS.md): current development stage, compatibility policy, path to 1.0, and known distribution limitations.
- [CHANGELOG](https://github.com/minoru-jp/shikumi/blob/main/CHANGELOG.md): major changes by public release.

Use the Glossary for concept meaning, the Specification for normative behavior, and the API Reference for name-oriented usage details.

## License

MIT License. See [`LICENSE`](https://github.com/minoru-jp/shikumi/blob/main/LICENSE).
