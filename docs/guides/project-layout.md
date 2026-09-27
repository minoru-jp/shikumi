# Project Layout and CLI

Shikumi does not require a dedicated distribution format or registration mechanism. If a regulation body, description body, or Realizer is importable as an ordinary Python object, it can be used from both library code and the CLI.

## Recommended role separation

Project-specific Shikumi code can live in ordinary Python packages chosen for the application. A dedicated name such as `shikumi_lib` is not required. The following split is only one way to keep responsibilities clear in a larger project.

| location | role |
| --- | --- |
| `shikumi_lib/norms/` | Regulation code such as Information Types, Descriptors, Structure, Validators, and Shikumi instances. |
| `shikumi_lib/realizers/` | Independent Realizers that transform Semantic Views into artifacts. |
| application package | The ordinary description body being validated or realized. It does not need to live under `shikumi_lib`. |

A small project may keep these roles in one module. A larger project may distribute them across separate libraries. The important property is not the physical name, but that the required objects can be obtained through normal Python imports.

## The CLI wires Python references

The CLI accepts `MODULE:OBJECT` references for Shikumi instances and Realizers, and `MODULE` or `MODULE:OBJECT` references for description bodies.

From this repository, the structure showcase can validate its actual package tree directly:

```bash
python -m shikumi validate \
  --shikumi structure_showcase.specification:showcase \
  --body structure_showcase.valid.combined \
  --at . \
  --structure-spec structure_showcase.specification:showcase_structure \
  --format text
```

`realize` wires a Realizer through the same `MODULE:OBJECT` reference style, but the official showcase intentionally focuses on structural regulation and does not define a Realizer. `realize` does not implicitly perform Validation or a Realizability check. Run the operations separately when they are required by your workflow.

## Distribution

Regulation bodies and Realizers can be distributed as Python code independently of Shikumi itself. They may live in the same distribution or in separate libraries.

The structure showcase in the Shikumi repository is learning material. It lives under `examples/` in the repository and is bundled under `shikumi/_examples/` in wheels so it remains separate from the public import surface that user code should depend on.
