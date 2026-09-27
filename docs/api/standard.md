# Standard API

Public API in `shikumi.standard`, built by composing Core's public semantic primitives.

related: [API_003](../specification/public-api.md#api_003), [API_004](../specification/public-api.md#api_004)

## `shikumi.standard`

Standard provides reusable concrete functionality composed from Core's public API. Standard does not introduce a new semantic model.

name: shikumi.standard

kind: Namespace

### `assignment()`

```python
def assignment(information_type: InformationType[T])
```

Returns a standard `@=` Descriptor that attaches the supplied value unchanged as Information of the specified Information Type. A Descriptor Use is also recorded when it is used.

```python
from shikumi import InformationType, information_of
from shikumi.standard import assignment

Title = InformationType("title", str)
title = assignment(Title)

class Page:
    title @= "Overview"

assert information_of(Page)[0].value == "Overview"
```

Consecutive `@=` operations under the same name are supported.

related: [DESC_003](../specification/description.md#desc_003)

name: assignment()

kind: Operation

input: information_type: InformationType[T]

output: descriptor supporting @=

### `decorator()`

```python
def decorator(information_type: InformationType[T])
```

Returns a simple value-taking Descriptor that attaches the supplied value unchanged as Information of the specified Information Type. A Descriptor Use is also recorded when the decorator is applied.

```python
from shikumi import InformationType, information_of
from shikumi.standard import decorator

Kind = InformationType("kind", str)
kind = decorator(Kind)

@kind("service")
class Service:
    pass

assert information_of(Service)[0].value == "service"
```

When vocabulary names themselves should remain directly traceable in an IDE, or arguments need custom meaning, define an ordinary Python decorator in the specification body instead of using this convenience function.

related: [DESC_003](../specification/description.md#desc_003)

name: decorator()

kind: Operation

input: information_type: InformationType[T]

output: value-taking decorator descriptor

### `DocstringWriter`

```python
DocstringWriter(
    information_type: InformationType[Any],
    *,
    clean: bool = True,
    required: bool = False,
)
```

A standard Descriptor that attaches the explicitly applied target's `__doc__` as Information. A Descriptor Use is recorded when it is applied, so the fact that the Descriptor was used remains even when no docstring exists.

With `clean=True`, excess indentation is removed according to Python's docstring-cleaning rules. With `required=True`, applying the writer to an object without a docstring raises `ValueError`.

related: [DESC_003](../specification/description.md#desc_003)

name: DocstringWriter

kind: Type

input: information_type: InformationType[Any], clean: bool = True, required: bool = False

### `docstring()`

```python
def docstring(
    information_type: InformationType[Any],
    *,
    clean: bool = True,
    required: bool = False,
) -> DocstringWriter
```

Convenience function that creates a `DocstringWriter`.

```python
from shikumi import information_of
from shikumi.standard import content_type, docstring

Content = content_type()
content = docstring(Content)

@content
class Overview:
    """Overview document."""

assert information_of(Overview)[0].value == "Overview document."
```

With `required=False`, nothing is attached when no docstring exists. Required presence of Information is generally best expressed as a Validation Rule.

related: [DESC_003](../specification/description.md#desc_003)

name: docstring()

kind: Operation

input: information_type: InformationType[Any], clean: bool = True, required: bool = False

output: DocstringWriter

### `content_type()`

```python
def content_type(
    name: str = "content",
    *,
    value_type: type[Any] | tuple[type[Any], ...] = str,
) -> InformationType[Any]
```

Convenience function that creates a `Cardinality.ONE` Information Type for primary content. `value_type` is passed through to the resulting `InformationType`.

name: content_type()

kind: Operation

input: name: str = "content", value_type: type[Any] | tuple[type[Any], ...] = str

output: InformationType[Any]

### `PackageTreeStructure`

```python
PackageTreeStructure()
```

When an already imported package is the Focus, explores its physical package tree, imports child packages and modules through Python's ordinary import mechanism, and constructs semantic structure.

When a module or entity is the Focus, it performs the same local interpretation as `PythonStructure`. In each module, lexically nested classes are included in semantic structure as entities in addition to classes directly under the module.

This Structure treats the results of Python imports as authoritative semantic state. It does not parse source as an AST. Modules discovered during package traversal execute through the normal import mechanism.

related: [STRUCT_001](../specification/structure.md#struct_001)

name: PackageTreeStructure

kind: Type

### `information_type_rule()`

```python
def information_type_rule(
    information_type: InformationType[Any],
    *,
    focus: StructuralKind = StructuralKind.ENTITY,
) -> ValidationRule
```

Creates a standard Validation Rule that checks the following for one Information Type:

- multiple values for `Cardinality.ONE`; and
- values that do not conform to `value_type`.

It does not require Information to be present or assign specification-specific meaning to values.

```python
from shikumi import InformationType, Shikumi
from shikumi.standard import assignment, information_type_rule

Title = InformationType("title", str)
title = assignment(Title)

class Page:
    title @= "First"
    title @= "Second"

docs = Shikumi(
    information_types=[Title],
    validators=[information_type_rule(Title)],
)
result = docs.validate(Page)

assert not result.is_valid
assert tuple(item.code for item in result.diagnostics) == (
    "information.cardinality",
)
```

related: [VAL_001](../specification/validation.md#val_001)

name: information_type_rule()

kind: Operation

input: information_type: InformationType[Any], focus: StructuralKind = StructuralKind.ENTITY

output: ValidationRule
