# Public API Boundary

Contracts for the import surface Shikumi exposes to users.

## API_001
The public Python API **MUST** consist of documented names exported from `shikumi` and `shikumi.standard`. Undocumented internal-module import paths are not public contracts.

title: Documented exports define the public surface

level: MUST

## API_002
Core (`shikumi`) owns Information, runtime binding, Structure, Semantic Views, Shikumi, Validation, and Realization abstractions.

title: Core owns the semantic primitives

level: INFORMATIVE

## API_003
Standard (`shikumi.standard`) **MUST** provide reusable concrete components built from Core and must not introduce a separate semantic model.

title: Standard builds on Core

level: MUST

## API_004
Standard **MUST NOT** implicitly define or register purpose-specific vocabulary such as `kind`, `attr`, or `rel`. Domain vocabulary belongs to the specification body.

title: Domain vocabulary belongs to the specification author

level: MUST NOT

related: [CORE_007](core.md#core_007)

## API_005
Shikumi does not guarantee compatibility handling for combinations of custom decorators, metaclasses, base classes, or mixins that alter ordinary Python class creation or Descriptor execution order.

title: Python class-creation interactions are outside compatibility guarantees

level: INFORMATIVE
