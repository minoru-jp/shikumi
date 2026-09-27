# Shikumi Glossary

This document defines Shikumi's canonical terminology and the semantic boundaries between its terms.

## Shikumi

A composition unit that interprets Python objects as one semantic system based on structure and information.

A Shikumi constructs a semantic view from an interpretation target and exposes that view in a form that can be used for validation and realization.

## Specification

The act of defining, and the resulting definitions of, how a target is described and interpreted in Shikumi, including structure, information types, descriptors, descriptor-use rules, and validation rules.

A specification defines the rules and forms that make descriptions meaningful information rather than defining the concrete content of a description itself.

## Specification Body

A Python `package` or `module` that concretely expresses a specification as Python code.

A specification body may contain definitions that make up a Shikumi specification, including structures, information types, descriptors, descriptor-use rules, and validation rules.

## Description

The act of assigning semantic information to an interpretation target or entity in Python code according to a specification, and the content so expressed.

A description becomes information through descriptors or other runtime processing.

## Description Body

A Python `package` or `module` that contains descriptions.

A description body contains entities on which information is described and may serve as both material for interpretation and a focus of Shikumi.

## Interpretation Target

A target interpreted by Shikumi.

It may include runtime objects such as Python `package`s, `module`s, and `class`es, as well as file placement needed to interpret structure.

## Structure

The placement, containment, and positional relationships of elements contained in an interpretation target.

Structure determines where `package`s, `module`s, entities, and other elements are located within a semantic system.

## Structure Specification

A specification of the required relative placement and containment relationships of `package`s, `module`s, and entities as seen from a focus.

A Structure Specification may be established explicitly by a specification body defining structural positions and kinds, or derived from the result of interpreting a description body as structure. The user explicitly chooses which form to use; Shikumi does not infer or substitute one when the other is absent.

Validation against a Structure Specification requires the structural range corresponding to the focus to match in position and kind. When validating a `module` independently as part of a larger whole, the intended structural placement of that module is specified explicitly and the corresponding subtree is validated.

A Structure Specification does not require the content of information attached to entities, the descriptors used, the description mechanism, or the import source to match. Conditions on where a descriptor may be used belong in descriptor-use rules; conditions on information content belong in information types or validation rules, separately from the Structure Specification.

## Physical Structure

Structure represented by file placement and the actual placement of Python `package`s and `module`s.

It deals with physical relationships among directories, files, `package`s, `module`s, and similar elements.

## Semantic Structure

The semantic structure established as a result of Shikumi interpreting an interpretation target.

Semantic structure represents the positional relationships in which Shikumi recognizes `package`s, `module`s, entities, and other elements.

## Entity

A unit treated as an independently information-bearing target in semantic structure.

Runtime objects such as Python `class`es may be interpreted as entities. What counts as an entity is determined by the structure.

## Information Type

The type of semantic information handled by Shikumi.

An Information Type defines semantic properties of information such as its value type and cardinality. It does not include how the information is written in Python.

## Information

One item of semantic information recorded on an interpretation target or entity.

Information has an Information Type, a value, and a subject to which it is attached. The fact that a descriptor was used is not part of the Information itself; it is handled separately as a Descriptor Use.

## Information Attachment

The act of associating a value or state produced by a description with an interpretation target or entity as Information and making it recognizable to Shikumi.

The specification determines what value is attached, under which Information Type, and to which subject. A descriptor makes a description into runtime Information through Information Attachment.

If the entity to receive the attachment does not yet exist at description time, attachment processing may be deferred until after the entity has been created. The concrete deferral mechanism belongs to the implementation of Information Attachment.

## Descriptor

A mechanism on the specification side that turns a description in Python code into Information.

A Descriptor may use `@=`, decorators, docstrings, or any other description form. Its definition determines the form, arguments, and construction of values; Shikumi does not prescribe these details.

A Descriptor can use Information Attachment to attach Information produced by a description to an interpretation target or entity. Independently of the Descriptor's concrete syntax and information values, a specification may define structural positions where that Descriptor is allowed or recommended.

## Descriptor Use

The runtime fact that a particular Descriptor was used on a particular interpretation target or entity.

A Descriptor Use is distinct from the Information attached by the Descriptor. One Descriptor Use may produce zero, one, or multiple Information Attachments, and Information may also be attached directly without a Descriptor Use.

Descriptor Use does not track a Descriptor's import source or its source-code spelling. Shikumi treats a Descriptor Use established after Python execution as semantic state for validating its relationship to structural position.

## Descriptor Use Rule

A specification of where in semantic structure a Descriptor is allowed or recommended to be used.

A Descriptor Use Rule does not define the content of Information generated or attached by the Descriptor. It evaluates the relationship between a Descriptor Use and the structural position of its subject, and can report use at a disallowed position or use at an allowed but non-recommended position as diagnostics.

A Descriptor for which no Descriptor Use Rule is defined is not structurally constrained by this mechanism. Its treatment is not inferred from information content or import source.

## Interpretation

The process by which Shikumi reads an interpretation target in terms of structure, Information, and Descriptor Uses and constructs a Semantic View.

Interpretation operates on objects, Information, and Descriptor Uses established by Python execution.

## Semantic View

A semantic observation produced by Shikumi by interpreting a particular Focus.

A Semantic View provides the semantic information used by validation and realization, including structure, entities, Information, Descriptor Uses, indexes, and related data centered on the Focus.

Even when an Information value holds another entity, a `module`, a function, or another Python object, that value is not automatically given Shikumi-specific reference semantics. How such a value is interpreted and used is defined by the specification.

## Focus

A position or structural unit placed at the semantic center when Shikumi constructs a Semantic View.

An entity, `module`, `package`, directory, or similar target may be used as a Focus. The Semantic View is constructed around that Focus, and the structure and information included depend on the structure and the nature of the operation.

A Focus may be accompanied by an intended structural placement when necessary. In particular, when validating a `module` independently, Shikumi does not infer placement from the current import name; the intended placement of the module must be specified explicitly.

## Validation

The process of determining whether a Semantic View satisfies defined conditions.

Validation operates on semantic state established by Python execution.

## Validation Rule

An individual rule that participates in Validation.

A Validation Rule defines the Focus needed for evaluation and the conditions applied to the Semantic View constructed for that Focus.

## Diagnostic

Information representing a problem or state observed by validation or another operation in a form that can be reported to the user.

A Diagnostic may carry an identifier, severity, subject, description, and similar data.

## Invariant

A condition that must always hold for Shikumi's semantic system or runtime mechanism to remain valid.

A state that violates an Invariant is distinguished from ordinary nonconformance found during Validation.

## Realization

The process of transforming a Semantic View into an Artifact.

## Realizer

An object that reads a Semantic View and generates an Artifact.

A Realizer uses the semantic representation of Information and Structure. A Realizer is independent of both the specification body and Shikumi itself; multiple Realizers may be applied to the same Semantic View.

A Realizer provides a way to ask whether it can realize a given Semantic View without generating the Artifact.

## Realizability

The property of whether a particular Realizer can generate an Artifact from a given Semantic View.

Realizability is independent of conformance to a specification. A description body may satisfy the specification and Structure Specification while still lacking information or conditions required by a particular Realizer. Realizability is determined without generating the Artifact.

## Artifact

A result generated by Realization.

An Artifact may take the form of Markdown, HTML, JSON, a graph, a string, another Python value, or another representation.

## Runtime Determination Principle

The principle that Shikumi's semantic state is determined from the state established after Python execution.

Python objects, Information, and Descriptor Uses produced as results of executing descriptors, decorators, `@=`, function calls, `import`, and other runtime behavior are the inputs to Interpretation.

## Logical Structure Element

A structural element in a Structure Specification that applies one regulation to multiple concrete elements that share the same structural role without fixing each concrete name in advance.

A Logical Structure Element has a logical name, parent position, Structure Fragment, and optional allowed-name and cardinality constraints. It does not dispatch among different regulations through wildcards, prefixes, regular expressions, or similar name-pattern mechanisms. At one parent, at most one Logical Structure Element may regulate each `StructuralKind`; logical elements for different kinds may coexist. Concrete elements resolved under the same parent and kind follow the same regulation.

## Structure Fragment

A self-contained root-relative partial structural regulation that can be reused as part of a Structure Specification.

A Structure Fragment can be mounted at concrete structural positions and can also serve as the regulation applied to each concrete instance of a Logical Structure Element. The same fragment may be lazily reapplied to recursive children to regulate structures of arbitrary observed depth. A normal Structure Fragment is closed and does not allow undescribed descendants. When descendant topology should be unrestricted, the fragment must explicitly be unconstrained.

## Structure Group

A regulation that treats several exact structural elements directly below the same parent as one set and constrains the minimum and maximum number of those members that may be present.

A Structure Group does not choose or replace the regulation applied to each member. Every member retains its own `StructuralKind`, required/optional status, and Structure Fragment; the group constrains only aggregate cardinality across that set.
