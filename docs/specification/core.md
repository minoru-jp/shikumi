# Core Semantics

Contracts shared by Shikumi's semantic model.

## CORE_001
Shikumi **MUST** interpret runtime objects, Information, and Descriptor Uses that exist after Python execution.

title: Runtime state is the source of interpretation

level: MUST

## CORE_002
Shikumi **MUST NOT** parse Python source as an AST to reconstruct semantic state from source text.

title: No AST-based semantic reconstruction

level: MUST NOT

## CORE_003
Information and Descriptor Uses **MUST** be treated as runtime facts independent of any Shikumi instance.

title: Runtime semantic state is independent of Shikumi instances

level: MUST

detail: Multiple Shikumi instances may interpret the same runtime objects according to the Information Types and rules each instance recognizes.

## CORE_004
A Semantic View **MUST** include only Information Types recognized by that Shikumi, and unrecognized Information **MUST NOT** be deleted from runtime objects.

title: Interpret recognized information without mutating unknown information

level: MUST

## CORE_005
Validation and realization **MUST** remain separate operations over a Semantic View.

title: Validation and realization are separate operations

level: MUST

## CORE_006
A Realizer **MUST NOT** be owned or registered by a Shikumi. Multiple Realizers may independently consume the same Semantic View.

title: Realizers are independent consumers

level: MUST

## CORE_007
Shikumi does not infer domain meaning automatically. Specification authors define the Information Types, Descriptor Use Rules, Validation Rules, and Structure that form a semantic system.

title: Meaning is author-defined

level: INFORMATIVE

## CORE_008
A `SemanticView` **MUST** be constructed from one structure resolution and one acquisition of runtime facts. Its subviews, and child-rule evaluation within the same validation operation, reuse the nodes, Information, and Descriptor Uses already captured rather than reinterpreting runtime state.

title: Semantic views preserve one interpreted runtime snapshot

level: MUST
