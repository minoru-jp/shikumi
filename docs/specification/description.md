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
For `@=` descriptions whose target class does not yet exist, `class_binding()` **MUST** defer the supplied value until class creation and then invoke the callback with the owner class and value.

title: Class binding defers connection until class creation

level: MUST
