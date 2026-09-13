# Placement of Specification Bodies, Description Bodies, and Realizers

This guide shows how to place specification bodies, description bodies, and Realizers so that they can ultimately be referenced from the CLI through ordinary Python imports.

Shikumi does not require a dedicated distribution format or registration mechanism. What matters is that the Python objects you use are importable and can be referenced from the CLI.

## Goal

The CLI accepts objects such as the `Shikumi` exposed by a specification body, a description body, and a Realizer as Python references in `MODULE:OBJECT` form.

The goal of placement is therefore not to convert these elements into a Shikumi-specific format. It is to keep them importable as ordinary Python modules or packages while making their roles easy to understand.

Specification bodies, description bodies, and Realizers are roles rather than physical formats. They may be included in the same module, package, or distribution.

## Recommended layout

In the official examples, project-specific Shikumi code is grouped in a `shikumi_lib` package and divided into `norms` and `realizers`.

```text
project/
├─ shikumi_lib/
│  ├─ __init__.py
│  ├─ norms/
│  │  ├─ __init__.py
│  │  └─ ...
│  └─ realizers/
│     ├─ __init__.py
│     └─ ...
└─ application/
   └─ ...
```

Place information types, descriptors, structures, validation rules, `Shikumi` instances, and other definitions used as a specification body under `norms`. Place Realizers that produce artifacts from semantic views under `realizers`.

A description body is the ordinary Python module or package being validated or realized. It does not need to be moved under `shikumi_lib`.

The name `shikumi_lib` is an example that avoids colliding with Shikumi's own import package, `shikumi`, while making project-specific Shikumi code recognizable at a glance.

## Referencing from the CLI

Assume the following layout:

```text
myproject/
├─ shikumi_lib/
│  ├─ norms/
│  └─ realizers/
└─ application/
```

For validation, specify the specification body and description body through ordinary import paths.

```bash
shikumi validate \
  --shikumi myproject.shikumi_lib.norms:app \
  --body myproject.application \
  --structure-spec myproject.shikumi_lib.norms:structure \
  --format text
```

For realization, additionally specify a Realizer.

```bash
shikumi realize \
  --shikumi myproject.shikumi_lib.norms:app \
  --body myproject.application \
  --realizer myproject.shikumi_lib.realizers.markdown:markdown \
  --output OUTPUT.md \
  --format json
```

Once the required objects can be referenced from the CLI, the placement goal has been achieved.

## Freedom of placement and distribution

`shikumi_lib/norms` and `shikumi_lib/realizers` are recommended examples intended to make roles easy to recognize. They are not requirements imposed by Shikumi.

A small setup may use a single module. Multiple roles may be included in the same distribution or distributed as separate libraries. Names and boundaries may be changed as part of ordinary Python library design.

Independently authored Specification bodies and Realizers can be distributed separately from Shikumi under licenses chosen by their authors, subject to the licenses of any third-party code they include.

The official examples are bundled in the main distribution as reference source. The examples themselves are not a public import package or CLI entry point. They live under `examples/` in the repository and under `shikumi/_examples/` in the wheel, keeping them separate from the public surface that user code can depend on.

In actual user projects, the required objects only need to be obtainable through ordinary Python imports and explicitly referenceable where they are used.
