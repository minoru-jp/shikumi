# Web API DSL

This end-to-end example combines custom information types and descriptors to build a small Web API DSL, then carries it through validation and Markdown realization.

Endpoint classes describe method, path, tags, content, and related endpoints as information. Validation rules run at entity, module, and package focus levels to check route shape and duplicates.

## Try it

From a repository checkout, put `examples/` on the Python path and use ordinary Python code to try validation and Markdown realization.

```python
from web_api import api
from web_api.shikumi_lib.norms import web_api, web_api_structure
from web_api.shikumi_lib.realizers.markdown import markdown

result = web_api.validate(api, structure_specification=web_api_structure)
assert result.is_valid
output = markdown.realize(result.view)
```

The example itself is distributed as reference source. It is not a public import package or CLI entry point.

## What to look at

- `@=`, docstrings, and class references are combined in one DSL.
- Descriptor-use rules explicitly restrict each descriptor to entities.
- The semantic view for the entire package is passed to a realizer, combining information from multiple modules into one artifact.
