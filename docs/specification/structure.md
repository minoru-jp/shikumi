# Structure Semantics

Contracts for interpreting runtime objects as package, module, and entity structure.

## STRUCT_001
`Structure.resolve()` **MUST** construct a `ResolvedStructure` whose nodes explicitly carry a subject, `StructuralKind`, and root-relative path.

title: Resolved structure is explicit

level: MUST

related: [CORE_001](core.md#core_001)

## STRUCT_002
`placement=None` **MUST** mean unspecified placement, while `()` explicitly means the structure-specification root. They must not be conflated.

title: Unspecified and root placement are distinct

level: MUST

## STRUCT_003
A standalone module may be interpreted as a view without a placement, but when `Shikumi.validate()` validates it in a context where its structural position matters, the intended placement **MUST** be specified.

title: Standalone module validation requires placement

level: MUST

condition: When a standalone module, rather than the whole package, is the Focus of `Shikumi.validate()`.

## STRUCT_004
A `StructureSpecification` **MUST** constrain placement and `StructuralKind`; it **MUST NOT** require matching Information values, Descriptor Uses, or description syntax.

title: Structure specification covers topology, not semantic content

level: MUST

## STRUCT_005
`StructureSpecification.from_resolved()` **MUST** be able to derive a specification that preserves relative placements and `StructuralKind` values from a resolved structure.

title: Structure specifications may be derived from resolved structure

level: MUST

## STRUCT_006
An explicit `StructureSpecification` and structure derived from another body are separate user-selected sources. Failure of one **MUST NOT** implicitly fall back to the other.

title: No implicit structure-source fallback

level: MUST NOT

## STRUCT_007
`StructureElement`, `StructureSpecification.elements`, `element_at()`, `subtree()`, and `from_resolved()` **MUST** retain concrete exact-path semantics. Logical names and wildcards must not be mixed into the meaning of the existing path tuples.

title: Exact structure API retains concrete-path semantics

level: MUST

## STRUCT_008
A `StructureFragment` **MUST** be reusable as a self-contained root-relative partial regulation. When a fragment is mounted at a concrete position, its exact elements **MUST** have the same meaning as `StructureElement`s expanded relative to that position.

title: Structure fragments compose without changing exact semantics

level: MUST

## STRUCT_009
A `LogicalStructureElement` **MUST** apply the same structural regulation to multiple concrete instances with different names under one parent position. When both an explicit `StructureElement` and a logical element could accept the same concrete name, the explicit `StructureElement` **MUST** take precedence.

title: Explicit structure overrides logical-name regulation

level: MUST

## STRUCT_010
A parent position **MUST NOT** define multiple `LogicalStructureElement`s for the same `StructuralKind`. Logical elements for different kinds may coexist and are selected by the observed kind. Shikumi **MUST NOT** dispatch among multiple logical regulations by prefix, suffix, glob, regular expression, arbitrary predicate, or another name-pattern mechanism.

title: Logical-name resolution is kind-disjoint and pattern-free

level: MUST NOT

detail: Names requiring different regulations should be modeled as exact `StructureElement`s or separated structurally in the specification body.

## STRUCT_011
A `LogicalStructureElement` **MUST** be able either to accept unrestricted concrete names or to restrict them to an enumerated set, and **MUST** be able to constrain the minimum and maximum number of instances resolved directly below the same parent.

title: Logical elements may constrain names and cardinality

level: MUST

## STRUCT_012
A closed structural regulation with no child rules **MUST** treat the position as a leaf. A regulation that imposes no topology constraints on descendants **MUST** state that explicitly with an unconstrained `StructureFragment`; existing closed semantics must not be changed implicitly.

title: Unconstrained subtrees are explicit

level: MUST

## STRUCT_013
`ResolvedStructure` **MUST** retain observed actual paths and **MUST NOT** rewrite them to the logical names of `LogicalStructureElement`s. Logical-to-actual correspondences are retained as bindings in the structure-check result.

title: Logical bindings do not rewrite resolved structure

level: MUST

## STRUCT_014
`Focus.placement` **MUST** use actual names even when the path traverses an instance of a `LogicalStructureElement`. Structure checking **MUST** resolve that actual path against the specification by applying explicit-element precedence followed by the logical element.

title: Placement remains an actual path through logical structure

level: MUST

## STRUCT_015
A `StructureElement` **MUST** distinguish required and optional exact elements without changing exact-path semantics. When an exact element with `required=False` is absent, its subtree regulation **MUST NOT** be activated. When it is present, the exact regulation **MUST** take precedence over a `LogicalStructureElement`, and required descendants and logical cardinality below it **MUST** be checked normally. The root `()` **MUST NOT** be optional.

title: Optional exact elements activate their subtree only when present

level: MUST

## STRUCT_016
When multiple `LogicalStructureElement`s share one parent, structure checking **MUST** select the logical regulation whose fragment root `StructuralKind` matches the actual child kind. Exact elements retain precedence, and no additional name-string dispatch may be introduced.

title: Logical regulations may differ by structural kind

level: MUST

## STRUCT_017
A recursive `StructureFragment` **MUST NOT** be pre-expanded into an infinite regulation. The same fragment regulation **MUST** instead be reapplied lazily to recursive children actually observed in the runtime structure. Recursive children have an implicit minimum count of zero so a finite runtime structure is never required to descend forever.

title: Recursive fragments are lazily reapplied

level: MUST

## STRUCT_018
A `StructureGroup` **MUST** constrain only the number of listed exact `StructureElement` siblings present below one parent. It **MUST NOT** replace each member's kind, required/optional status, or fragment regulation, and **MUST NOT** be used for regulation selection or name dispatch.

title: Structure groups constrain sibling cardinality only

level: MUST

