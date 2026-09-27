# Structure Showcase

This example is intentionally domain-light. Instead of modeling an application such as a web API or an architecture, it shows general structural patterns that Shikumi can regulate in one executable fixture set.

The regulation lives in [`specification.py`](./specification.py). [`valid/`](./valid/) contains package trees that must be accepted, while [`invalid/`](./invalid/) contains deliberate violations. Every fixture is an ordinary Python package, so `PackageTreeStructure` resolves the actual package tree before the `StructureSpecification` is checked.

## Structural patterns included

- required and optional exact elements
- logical elements with free names, enumerated names, and cardinality
- arbitrary package and module names under the same parent, selected by `StructuralKind`
- reusable `StructureFragment` composition and unconstrained subtrees
- arbitrary-depth recursion through `StructureFragment.recursive()`
- heterogeneous exact-sibling cardinality through `StructureGroup`
- exact-element precedence over a logical element at the same parent

## Fixture layout

`valid/minimal/` contains only the required element. `valid/combined/` combines all of the patterns above in one package tree.

`invalid/` separates several failure modes: a missing required element, an empty logical collection, a name outside an enumerated set, a group-cardinality violation, and an extra element inside a closed logical branch. These are executable negative examples, and their diagnostic codes are fixed by tests.

## Try it

From a repository checkout, put `examples/` on the Python path and run:

```python
from structure_showcase.invalid import group_both
from structure_showcase.specification import showcase, showcase_structure
from structure_showcase.valid import combined

valid_result = showcase.validate(
    combined,
    placement=(),
    structure_specification=showcase_structure,
)
assert valid_result.is_valid
assert valid_result.structure_check is not None
assert {binding.logical_element.logical_name for binding in valid_result.structure_check.bindings} >= {
    "entry",
    "variant",
    "package_child",
    "module_child",
    "branch",
    "module_leaf",
    "ordinary",
}

invalid_result = showcase.validate(
    group_both,
    placement=(),
    structure_specification=showcase_structure,
)
assert not invalid_result.is_valid
assert {diagnostic.code for diagnostic in invalid_result.diagnostics} == {
    "structure.group.maximum",
}
```
