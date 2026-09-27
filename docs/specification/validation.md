# Validation Semantics

Contracts for Validation over a Semantic View.

## VAL_001
A `ValidationRule` **MUST** evaluate a Semantic View and return zero or more Diagnostics. Validation must diagnose rather than automatically repair runtime state.

title: Validation diagnoses without repair

level: MUST

## VAL_002
`ValidationResult.is_valid` **MUST** be true exactly when there are no `ERROR` Diagnostics. Warnings and informational Diagnostics do not make the result invalid.

title: Validity is determined by error diagnostics

level: MUST

## VAL_003
A `DescriptorUseRule` **MUST** report an error when `allowed` does not match, and a warning when `allowed` matches but `recommended` does not.

title: Descriptor-use rule severity

level: MUST

related: [DESC_003](description.md#desc_003)

## VAL_004
Structural validation **MUST** compare placement and `StructuralKind` for the portion of the `StructureSpecification` corresponding to the current focus.

title: Structural validation compares the focused subtree

level: MUST

related: [STRUCT_004](structure.md#struct_004)

## VAL_005
`Shikumi.validate()` **MUST** aggregate view construction, Descriptor Use checks, an optional structure check, and registered Validation Rules into one `ValidationResult`.

title: Shikumi validation aggregates semantic checks

level: MUST

## VAL_006
Validation **MUST NOT** implicitly run `Realizer.check()`. Realizer-specific realizability is independent of conformance to a Shikumi specification.

title: Validation does not imply realization checks

level: MUST NOT

## VAL_007
Within closed portions of the selected `StructureSpecification`, structure checking **MUST** report missing required elements, `StructuralKind` mismatches, and unspecified additional elements as errors. A `LogicalStructureElement` applies the same closed fragment to each resolved actual instance. Only a subtree explicitly regulated by an unconstrained `StructureFragment` omits descendant-topology checks.

title: Structure checking is closed unless explicitly unconstrained

level: MUST

related: [STRUCT_004](structure.md#struct_004), [STRUCT_009](structure.md#struct_009), [STRUCT_012](structure.md#struct_012)

## VAL_008
When a `ValidationRule` returns a `Diagnostic` whose `subject` is `None`, the Focus subject of the `SemanticView` passed to that rule **MUST** be used as the Diagnostic subject.

title: Validation diagnostics default to the rule focus

level: MUST
