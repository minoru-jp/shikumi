# Deriving a structural regulation from a description body

This example derives a structure specification from interpreting one description body as a structure, then validates whether another description body conforms to that structure.

The first description body is used as the material from which a structural regulation for another body is derived. It is an ordinary Python package, not a special file format.

## Try it

From a repository checkout, put `examples/` on the Python path and use the example as ordinary Python code.

```python
from structure_from_body import candidate, reference
from structure_from_body.shikumi_lib.norms import structure_only

specification = structure_only.derive_structure_specification(reference)
result = structure_only.validate(candidate, structure_specification=specification)
assert result.is_valid
```

The structure specification is derived from the `reference` package and used to validate the `candidate` package. Validation succeeds because they have the same module/class layout.

## What it does not validate

This mechanism validates conformance to the structure specification. Shikumi does **not** by itself verify that the contents or meaning of the two description bodies match.

The example intentionally gives `reference.catalog.ITEM_1` and `candidate.catalog.ITEM_1` completely different docstrings. Structural validation still succeeds because their structures match.

A typical application is to derive a structure specification from an original document and confirm that a translated version has the same heading structure. If semantic accuracy of the translation must also be checked, those conditions need to be defined separately as application-specific information types or validation rules. Applying the same structure specification to two description bodies with intentionally different content is perfectly valid.
