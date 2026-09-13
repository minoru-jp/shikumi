# Structured-document realization

This example constructs a semantic view from Python descriptions and realizes it as Markdown with an independent realizer.

Command names, categories, and docstring content are each treated as information types. Validation checks whether the description satisfies the regulation, while the Markdown realizer produces a publishable listing from the same semantic view.

## Try it

From a repository checkout, put `examples/` on the Python path and use ordinary Python code to try validation and realization.

```python
from structured_docs import body
from structured_docs.shikumi_lib.norms import structured_docs
from structured_docs.shikumi_lib.realizers.markdown import markdown

result = structured_docs.validate(body)
assert result.is_valid
output = markdown.realize(result.view)
```

`output` contains Markdown describing the `deploy` and `status` commands.

## What to look at

- `@command(...)`, `category @= ...`, and docstrings use different Python notation but appear as information in the same semantic view.
- The realizer is not registered with Shikumi. It is an independent component that receives a semantic view.
- Realizability checking with `check()` and realization with `realize()` are separate operations.
