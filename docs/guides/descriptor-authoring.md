# Defining Descriptors

Shikumi does not prescribe a concrete Descriptor syntax. Specification authors define Descriptors with ordinary Python and explicitly record the runtime facts their Descriptors establish.

## Decorators without arguments

A Descriptor can record both Descriptor Use and Information Attachment in an ordinary Python method, preserving normal IDE navigation, docstrings, and type annotations.

```python
from shikumi import (
    Cardinality,
    InformationType,
    attach_information,
    descriptor_uses_of,
    information_of,
    record_descriptor_use,
)

Kind = InformationType("kind", str, cardinality=Cardinality.MANY)

class KindDescriptions:
    def attr(self, subject):
        record_descriptor_use(subject, self.attr)
        attach_information(subject, Kind, "attr")
        return subject

    def service(self, subject):
        record_descriptor_use(subject, self.service)
        attach_information(subject, Kind, "service")
        return subject

kind = KindDescriptions()

@kind.attr
class Owner:
    pass

@kind.service
class UserService:
    pass

assert [record.value for record in information_of(Owner)] == ["attr"]
assert descriptor_uses_of(UserService)[0].subject is UserService
```

## Decorators with arguments

The Descriptor author owns the arguments, return values, and decorator-factory shape. Shikumi does not infer Information from function signatures.

```python
from shikumi import (
    Cardinality,
    InformationType,
    attach_information,
    information_of,
    record_descriptor_use,
)

Uses = InformationType("uses", type, cardinality=Cardinality.MANY)

class RelationDescriptions:
    def uses(self, target: type):
        def decorate(subject):
            record_descriptor_use(subject, self.uses)
            attach_information(subject, Uses, target)
            return subject
        return decorate

relation = RelationDescriptions()

class UserRepository:
    pass

@relation.uses(UserRepository)
class UserService:
    pass

assert information_of(UserService)[0].value is UserRepository
```

## Custom `@=` Descriptors

When `@=` is evaluated, the target class does not yet exist. `class_binding()` runs its callback during class creation, after the class body has finished executing and before `__init_subclass__()`. The current implementation realizes this timing through `__set_name__()`, so the callback must not depend on state added by `__init_subclass__()`. Repeated `@=` writes under the same binding name are replayed in source order. Shikumi does not normalize callback exceptions: Python 3.11 wraps an exception raised from `__set_name__()` in `RuntimeError`, while Python 3.12 and later propagate the original exception with a runtime note.

`@=` is one possible syntax for a custom Descriptor; Shikumi Core does not require it. In the normal authoring flow, the writer held in the outer namespace is not consumed. Each class body receives its own temporary binding under that name. Aliasing or directly reusing the binding object itself outside this authoring pattern is not part of the public contract.

```python
from shikumi import (
    Cardinality,
    ClassBinding,
    InformationType,
    attach_information,
    class_binding,
    information_of,
    record_descriptor_use,
)

Tag = InformationType("tag", str, cardinality=Cardinality.MANY)

class TagDescriptions:
    def __imatmul__(self, value: str) -> ClassBinding[str]:
        return class_binding(value, self._connect)

    def _connect(self, subject: type[object], value: str) -> None:
        record_descriptor_use(subject, self)
        attach_information(subject, Tag, value)

tag = TagDescriptions()

class UserService:
    tag @= "application"
    tag @= "users"

assert [record.value for record in information_of(UserService)] == [
    "application",
    "users",
]
```

## Combining a Descriptor Use Rule

Use `DescriptorUseRule` and `StructureSelector` when a Descriptor is allowed or recommended only at particular structural locations. This is independent from validating the Information values produced by the Descriptor.

```python
from shikumi import (
    DescriptorUseRule,
    InformationType,
    Shikumi,
    StructuralKind,
    StructureSelector,
)
from shikumi.standard import decorator

Kind = InformationType("kind", str)
service = decorator(Kind)

service_rule = DescriptorUseRule(
    descriptor=service,
    allowed=StructureSelector(kind=StructuralKind.ENTITY),
    recommended=StructureSelector(
        kind=StructuralKind.ENTITY,
        under=("api",),
    ),
    name="service",
)

system = Shikumi(
    information_types=[Kind],
    descriptor_rules=[service_rule],
)

@service("service")
class Endpoint:
    pass

result = system.validate(Endpoint)
assert result.is_valid
```
