# Realization Semantics

Contracts for turning a Semantic View into an artifact.

## REAL_001
`Realizer.realize()` **MUST** consume a Semantic View and return an artifact. Shikumi Core does not restrict the artifact's Python type.

title: Realizer consumes a semantic view

level: MUST

related: [CORE_005](core.md#core_005)

## REAL_002
`Realizer.check()` **MUST** report Realizer-specific realizability without generating the artifact.

title: Check does not realize

level: MUST

## REAL_003
`RealizationCheck.is_realizable` **MUST** be true exactly when no `ERROR` Diagnostic is present.

title: Realizability is determined by error diagnostics

level: MUST

## REAL_004
A Realizer **MUST** remain independent of a Shikumi instance, and multiple Realizers may consume the same Semantic View.

title: Realizers remain independent

level: MUST

related: [CORE_006](core.md#core_006)

## REAL_005
A Realizer **MAY** add output-specific conditions through `check()`, but those checks are not an implicit substitute for core Validation.

title: Realizer checks may add output-specific conditions

level: MAY

## REAL_006
When a `RealizationCheck` receives a `Diagnostic` whose `subject` is `None`, the Focus subject of the checked `SemanticView` **MUST** be used as the Diagnostic subject.

title: Realization diagnostics default to the view focus

level: MUST
