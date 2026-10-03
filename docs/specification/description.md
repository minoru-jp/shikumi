# Description Semantics

Contracts for turning Python descriptions into runtime semantic state.

## DESC_001
An Information Type **MUST** define its semantic name, accepted Python value type, and cardinality, and its identity is the identity of the `InformationType` object.

title: Information type identity

level: MUST

related: [CORE_003](core.md#core_003)

## DESC_002
Information Attachment **MUST** associate a subject, Information Type, and value as one runtime Information record. Attachment does not reject multiple values merely because the cardinality is `ONE`.

title: Attachment preserves observable runtime state

level: MUST

detail: Cardinality violations remain observable so Validation can diagnose them.

## DESC_003
Descriptor Use and Information Attachment **MUST** remain distinct runtime facts. One Descriptor Use may attach zero, one, or many Information records.

title: Descriptor use and information attachment are distinct

level: MUST

## DESC_004
Descriptor syntax **MAY** use decorators, `@=`, docstrings, ordinary function calls, or other runtime Python mechanisms.

title: Description syntax is open

level: MAY

## DESC_005
Shikumi **MUST NOT** infer Information or Descriptor Use Rules from Descriptor signatures, return values, import origins, or source-level names.

title: No descriptor inference

level: MUST NOT

related: [CORE_007](core.md#core_007)

## DESC_006
For `@=` descriptions whose target class does not yet exist, `class_binding()` **MUST** retain the supplied value until the class body has finished executing and invoke the callback during class creation, once the owner class is available and before `__init_subclass__()`, with the owner class and value.

title: Class binding defers connection until class creation

level: MUST

detail: Repeated `@=` writes under the same binding name are preserved in source order. The public typing contract represents the returned value as `ClassBinding[T]`, which accepts additional values of the same type as the initial value. In the normal authoring flow, the outer writer is not consumed; a temporary binding is placed in each class-body namespace. Shikumi does not normalize exceptions raised by the callback; their externally visible form follows the class-creation semantics of the Python runtime in use. The concrete temporary binding implementation, aliasing of that binding, and direct reuse of the binding object across multiple classes are not part of the public contract.
