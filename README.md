# Shikumi

Shikumi is a **library for building structured document generators, custom DSLs, architecture validators, and similar systems on top of Python**.

Shikumi itself does not provide those features as individual built-ins.

Instead, you define a specification that determines what elements exist, what attributes and relationships they have, what structure they belong to, what counts as a valid state, and what can be produced from the resulting semantic view.

For example, transforming the resulting semantic view into Markdown becomes document generation. Defining custom information types and description mechanisms such as `service`, `entity`, and `uses` creates a DSL. A rule such as "only dependencies from the application layer to the domain layer are allowed" becomes architecture validation.

In other words, Shikumi does not deal with architecture, DSLs, or documents themselves. It is a **common foundation for building systems with custom meaning and rules on top of Python, interpreting them, and using the result**.

## Main uses

Shikumi can be used, for example, to:

- generate documents, configuration, reports, and other artifacts from semantic views constructed from descriptions in Python code;
- create documents with explicit meaning and structure for rapid communication with LLMs;
- describe domain-specific attributes, classifications, and relationships on Python classes and modules;
- build a Python-based DSL with custom descriptors and information types;
- define the package, module, and class structure a project is expected to have;
- apply the same specification to multiple Python packages; and
- express software architecture structure and dependency directions, then build validation around them.

These uses are not built into Shikumi itself. They are created by defining a specification for the intended purpose.

## Installation

```bash
pip install shikumi
```

Current version: `0.1.0`.

Shikumi targets Python 3.11 and later.

## Quick start

The following example defines an information type named `title` and describes it through two kinds of descriptors: `@=` and a decorator.

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

`InformationType` defines **what something means**; descriptors define **how that meaning is written in Python**. `Shikumi` combines the information types, validation rules, descriptor-use rules, and other parts it recognizes, constructs a semantic view with `view()`, and validates it with `validate()`.

`title @= "Overview"` is not ordinary attribute assignment. The descriptor created by `assignment(Title)` attaches information to `Overview` after the class has been created. `@=` is a Standard notation for describing meaning defined by the specification while keeping a natural class-body form.

## Warning

**Only pass trusted Python modules and packages to Shikumi.**

Shikumi interprets objects that exist after Python execution. When a module or package is supplied by import path, it is imported and executed as ordinary Python before Shikumi constructs its semantic view. This is true whether that semantic view is used for validation, realization, or another operation. Target code can perform arbitrary actions with the same permissions as a normal import in the current Python process.

Be especially careful with validation: it is not a sandboxed or static safety check. Do not pass untrusted Python code to Shikumi in order to determine whether it is safe.

## Runtime determination principle

Shikumi does not re-read Python source as an AST. Modules and packages used as description bodies are imported as ordinary Python, and Shikumi observes the runtime objects, information, and descriptor uses that exist after execution.

```text
Python source
    ↓ execute / import
runtime objects + information + descriptor uses
    ↓
Shikumi
    ↓ interpretation
semantic view
   /          \
validation     realization
                  ↓
               artifact
```

Therefore, when a target module is loaded for validation, its top-level code is executed just as it is during a normal import. Shikumi is not a static analyzer that determines safety without executing the target.

## What Shikumi does not inspect automatically

Shikumi does not automatically analyze Python ASTs or source syntax, actual import or call graphs, or modules that have not been imported. The standard `PythonStructure` also does not treat functions or methods as entities. Model any additional information or targets explicitly in your norms or in a custom Structure.

## Validation and realization

Shikumi reads Python objects and the information attached to them according to a structure and constructs a semantic view.

Validation applies validation rules to that semantic view. You can define conditions for a specific purpose, such as whether a package contains required modules, whether a class has required information, or whether relationships between elements satisfy a rule.

A semantic view is not limited to validation. By applying an independent Realizer, it can be realized into arbitrary artifacts such as Markdown, configuration, or reports. Multiple Realizers can be applied to the same semantic view.

## Standard

`shikumi.standard` provides reusable concrete functionality built from Core mechanisms.

Its main facilities include `assignment` for `@=`, `decorator` for decorator-based description, `docstring` for turning docstrings into information, and `PackageTreeStructure` for interpreting a package tree through ordinary imports.

Purpose-specific meanings such as `service`, `entity`, `layer`, and `term` are not part of Standard. They are defined by the user's specification.

## CLI

The CLI can wire together a `Shikumi` exposed by a specification body, a description body, and an independent Realizer using ordinary Python imports.

The CLI entry point is `shikumi`. The same CLI is also available through `python -m shikumi`.

Validation:

```bash
shikumi validate \
  --shikumi myproject.shikumi_lib.norms:app \
  --body myproject.application \
  --structure-spec myproject.shikumi_lib.norms:app_structure \
  --format text
```

Realization:

```bash
shikumi realize \
  --shikumi myproject.shikumi_lib.norms:app \
  --body myproject.application \
  --realizer myproject.shikumi_lib.realizers.markdown:markdown \
  --output API.md \
  --format json
```

`realize` does not implicitly perform validation or a realizability check. These are treated as independent operations.

## Examples

[`examples/`](./examples/) contains four official examples that approach Shikumi from different directions. They are bundled in the distribution as reference source, but they are not a public import package or CLI entry point.

- [`architecture`](./examples/architecture/README.md) — define application-specific dependency rules and validate architecture
- [`structured_docs`](./examples/structured_docs/README.md) — construct a semantic view from Python descriptions and realize it as Markdown
- [`web_api`](./examples/web_api/README.md) — an end-to-end example combining a custom DSL, validation, and realization
- [`structure_from_body`](./examples/structure_from_body/README.md) — derive a structural regulation from one description body and validate another body for structural conformance

## Related documentation

- [`docs/glossary.md`](./docs/glossary.md) — Shikumi terminology and semantic boundaries
- [`docs/api-reference.md`](./docs/api-reference.md) — public API and its contracts
- [`docs/distribution-guide.md`](./docs/distribution-guide.md) — placement and distribution of specification bodies, description bodies, and Realizers
- [`CHANGELOG.md`](./CHANGELOG.md) — major changes by public release
- [`examples/`](./examples/) — four official examples also bundled in the distribution as reference source

For precise concept definitions, use the glossary as the reference.

## About the public documentation

All public documentation is provided in English. Canonical sources live under `_internal/document_source/`; `shikumi-devdoc` realizes committed Japanese intermediates under `_internal/document_build/ja/`, and those intermediates are used as the translation source for the public documents.

Intermediate files are generated artifacts and are not edited directly. If a public document, an intermediate document, and a canonical source differ, the canonical document source takes precedence.

## License

MIT License. See [`LICENSE`](./LICENSE).
