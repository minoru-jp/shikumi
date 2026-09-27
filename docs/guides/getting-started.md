# Getting Started

This guide walks through one complete cycle: describe semantic information on a Python class, construct a Semantic View with Shikumi, validate it, and finally realize it as a string.

The goal is not to cover the whole API. It is to make the responsibility boundaries visible in the smallest useful executable example.

## Complete example

```python
from shikumi import (
    Diagnostic,
    InformationType,
    Realizer,
    Shikumi,
    StructuralKind,
    validator,
)
from shikumi.standard import assignment, information_type_rule

Title = InformationType("title", str)
title = assignment(Title)


class Overview:
    title @= "Overview"


@validator(focus=StructuralKind.ENTITY)
def require_title(view):
    if not view.focused.has(Title):
        yield Diagnostic("title is required")


docs = Shikumi(
    information_types=[Title],
    validators=[require_title, information_type_rule(Title)],
)


class HeadingRealizer(Realizer[str]):
    def realize(self, view):
        value = view.focused.values(Title)[0]
        return f"# {value}\n"


result = docs.validate(Overview)
assert result.is_valid

markdown = HeadingRealizer().realize(result.view)
assert markdown == "# Overview\n"
```

The code deliberately defines four concerns separately: `Title` is an Information Type, `title` is a Descriptor, `require_title` is a Validator, and `HeadingRealizer` is an independent Realizer.

## Read the responsibilities separately

| part | responsibility |
| --- | --- |
| `InformationType` | Defines what a value means and what value type and cardinality it has. |
| Descriptor (`assignment`) | Connects a Python description to runtime Information. |
| `Shikumi` | Combines the recognized Information Types, Structure, Validators, and related rules into one interpretation system. |
| Validator | Applies application-specific conditions to an already constructed Semantic View. |
| Realizer | Reads a Semantic View and produces an artifact independently of the Shikumi instance. |

This separation is central to Shikumi. Meaning, Python syntax, validity, and artifact generation are not forced into one mechanism. An application composes the pieces it needs.

## Read next

- To define custom decorators or `@=` Descriptors, see [Defining Descriptors](./descriptor-authoring.md).
- To place regulations and Realizers in a project and wire them through the CLI, see [Project Layout and CLI](./project-layout.md).
- To look up individual public names, use the [API Reference](../api/INDEX.md).
- For exact contracts around runtime determination, Structure, Validation, and Realization, use the [Specification](../specification/INDEX.md).
