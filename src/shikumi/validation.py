"""Validation of semantic views around explicit runtime foci."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import TypeAlias

from .description import DescriptorUseRule, same_descriptor
from .structure import (
    Focus,
    LogicalStructureElement,
    ResolvedStructure,
    StructuralKind,
    StructureElement,
    StructureFragment,
    StructureGroup,
    StructureSpecification,
)
from .view import SemanticView


class DiagnosticSeverity(str, Enum):
    """Severity attached to one validation diagnostic."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True, slots=True)
class Diagnostic:
    """One reportable observation produced by validation."""

    message: str
    code: str | None = None
    severity: DiagnosticSeverity = DiagnosticSeverity.ERROR
    subject: object | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.message, str):
            raise TypeError("diagnostic message must be a string")
        if not self.message:
            raise ValueError("diagnostic message must not be empty")
        if self.code is not None and not isinstance(self.code, str):
            raise TypeError("diagnostic code must be a string or None")
        if self.code == "":
            raise ValueError("diagnostic code must not be empty")
        if not isinstance(self.severity, DiagnosticSeverity):
            raise TypeError("diagnostic severity must be a DiagnosticSeverity")


ValidationOutput: TypeAlias = Diagnostic | Iterable[Diagnostic] | None
ValidationFunction: TypeAlias = Callable[[SemanticView], ValidationOutput]


@dataclass(frozen=True, slots=True, eq=False)
class ValidationRule:
    """A condition evaluated with a semantic view of one required focus kind.

    Rules are identity-based. The rule declares the kind of focus it needs;
    validation decides which runtime subjects can naturally provide that focus.
    """

    focus_kind: StructuralKind
    check: ValidationFunction
    name: str

    def __post_init__(self) -> None:
        if not isinstance(self.focus_kind, StructuralKind):
            raise TypeError("validation rule focus_kind must be a StructuralKind")
        if not callable(self.check):
            raise TypeError("validation rule check must be callable")
        if not isinstance(self.name, str):
            raise TypeError("validation rule name must be a string")
        if not self.name:
            raise ValueError("validation rule name must not be empty")

    def __call__(self, view: SemanticView) -> tuple[Diagnostic, ...]:
        """Evaluate this rule against a view with the required focused kind."""

        if view.focused.kind is not self.focus_kind:
            raise ValueError(
                f"validation rule {self.name!r} requires focus kind "
                f"{self.focus_kind.value!r}, got {view.focused.kind.value!r}"
            )

        output = self.check(view)
        return tuple(self._normalize_output(output, view.focus))

    @staticmethod
    def _normalize_output(
        output: ValidationOutput,
        focus: Focus,
    ) -> Iterator[Diagnostic]:
        if output is None:
            return

        if isinstance(output, Diagnostic):
            yield ValidationRule._bind_subject(output, focus)
            return

        for diagnostic in output:
            if not isinstance(diagnostic, Diagnostic):
                raise TypeError("validation rules must yield Diagnostic objects")
            yield ValidationRule._bind_subject(diagnostic, focus)

    @staticmethod
    def _bind_subject(diagnostic: Diagnostic, focus: Focus) -> Diagnostic:
        if diagnostic.subject is not None:
            return diagnostic
        return replace(diagnostic, subject=focus.subject)


@dataclass(frozen=True, slots=True)
class StructureBinding:
    """Bind one logical structure element to one concrete runtime path."""

    logical_element: LogicalStructureElement
    actual_path: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.logical_element, LogicalStructureElement):
            raise TypeError(
                "structure binding logical_element must be a LogicalStructureElement"
            )
        if isinstance(self.actual_path, str):
            raise TypeError(
                "structure binding actual_path must be a tuple of path components"
            )
        normalized = tuple(self.actual_path)
        if not normalized:
            raise ValueError("structure binding actual_path must not be empty")
        if any(not isinstance(part, str) or not part for part in normalized):
            raise ValueError(
                "structure binding actual_path components must be non-empty strings"
            )
        object.__setattr__(self, "actual_path", normalized)

@dataclass(frozen=True, slots=True)
class StructureCheck:
    """Result of checking a resolved structure against a structural regulation."""

    specification: StructureSpecification
    placement: tuple[str, ...]
    diagnostics: tuple[Diagnostic, ...]
    bindings: tuple[StructureBinding, ...] = ()

    @property
    def is_valid(self) -> bool:
        return not any(
            diagnostic.severity is DiagnosticSeverity.ERROR
            for diagnostic in self.diagnostics
        )

    def __bool__(self) -> bool:
        return self.is_valid


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Diagnostics produced while validating one requested focus."""

    view: SemanticView
    diagnostics: tuple[Diagnostic, ...]
    structure_check: StructureCheck | None = None

    @property
    def is_valid(self) -> bool:
        """Return whether validation produced no error diagnostics."""

        return not any(
            diagnostic.severity is DiagnosticSeverity.ERROR
            for diagnostic in self.diagnostics
        )

    def __bool__(self) -> bool:
        return self.is_valid


def _effective_path(view: SemanticView, node_path: tuple[str, ...]) -> tuple[str, ...]:
    """Return a regulation-root-relative path for one node in *view*."""

    root_path = view.focused.node.path
    if node_path[: len(root_path)] != root_path:
        raise ValueError("semantic view contains a node outside its focus root")
    relative = node_path[len(root_path) :]
    if view.focus.placement is not None:
        return view.focus.placement + relative
    return relative


def check_descriptor_uses(
    view: SemanticView,
    rules: Iterable[DescriptorUseRule],
) -> tuple[Diagnostic, ...]:
    """Check recorded descriptor uses against structural usage rules."""

    normalized_rules = tuple(rules)
    diagnostics: list[Diagnostic] = []
    for item in view.items:
        path = _effective_path(view, item.node.path)
        for use in item.descriptor_uses:
            for rule in normalized_rules:
                if not same_descriptor(use.descriptor, rule.descriptor):
                    continue
                if not rule.allowed.matches(kind=item.kind, path=path):
                    diagnostics.append(
                        Diagnostic(
                            f"descriptor {rule.display_name!r} cannot be used at "
                            f"{StructureSpecification.format_path(path)} "
                            f"({item.kind.value})",
                            code="descriptor.use.disallowed",
                            subject=item.subject,
                        )
                    )
                    continue
                if rule.recommended is not None and not rule.recommended.matches(
                    kind=item.kind,
                    path=path,
                ):
                    diagnostics.append(
                        Diagnostic(
                            f"descriptor {rule.display_name!r} is allowed but not "
                            f"recommended at {StructureSpecification.format_path(path)} "
                            f"({item.kind.value})",
                            code="descriptor.use.not_recommended",
                            severity=DiagnosticSeverity.WARNING,
                            subject=item.subject,
                        )
                    )
    return tuple(diagnostics)


@dataclass(slots=True)
class _StructureRuleNode:
    kind: StructuralKind
    required: bool = True
    exact_children: dict[str, "_StructureRuleNode"] = field(default_factory=dict)
    logical_children: dict[StructuralKind, "_LogicalStructureRule"] = field(
        default_factory=dict
    )
    groups: tuple[StructureGroup, ...] = ()
    unconstrained: bool = False


@dataclass(slots=True)
class _LogicalStructureRule:
    element: LogicalStructureElement
    root: _StructureRuleNode


def _build_rule_tree(
    specification: StructureSpecification,
) -> _StructureRuleNode:
    memo: dict[int, _StructureRuleNode] = {}
    root, nodes = _build_rule_tree_parts(
        specification.elements,
        specification._unconstrained_paths,
        specification.groups,
    )
    _attach_logical_rules(nodes, specification.logical_elements, memo=memo)
    _attach_recursive_rules(
        nodes,
        specification._recursive_elements,
        owner_fragment=None,
        memo=memo,
    )
    return root


def _build_fragment_rule_tree(
    logical: LogicalStructureElement,
    memo: dict[int, _StructureRuleNode] | None = None,
) -> _StructureRuleNode:
    return _build_fragment_tree(logical.fragment, memo=memo)


def _build_fragment_tree(
    fragment: StructureFragment,
    *,
    memo: dict[int, _StructureRuleNode] | None = None,
) -> _StructureRuleNode:
    if memo is None:
        memo = {}
    identity = id(fragment)
    if identity in memo:
        return memo[identity]

    root, nodes = _build_rule_tree_parts(
        fragment.elements,
        fragment._unconstrained_paths,
        fragment.groups,
    )
    memo[identity] = root
    _attach_logical_rules(nodes, fragment.logical_elements, memo=memo)
    _attach_recursive_rules(
        nodes,
        fragment._recursive_elements,
        owner_fragment=fragment,
        memo=memo,
    )
    return root


def _build_rule_tree_parts(
    elements: tuple[StructureElement, ...],
    unconstrained_paths: tuple[tuple[str, ...], ...],
    groups: tuple[StructureGroup, ...],
) -> tuple[_StructureRuleNode, dict[tuple[str, ...], _StructureRuleNode]]:
    nodes: dict[tuple[str, ...], _StructureRuleNode] = {}
    for element in elements:
        nodes[element.path] = _StructureRuleNode(
            kind=element.kind,
            required=element.required,
        )

    for path, node in nodes.items():
        if not path:
            continue
        parent = nodes[path[:-1]]
        parent.exact_children[path[-1]] = node

    for path in unconstrained_paths:
        nodes[path].unconstrained = True

    groups_by_parent: dict[tuple[str, ...], list[StructureGroup]] = {}
    for group in groups:
        groups_by_parent.setdefault(group.parent, []).append(group)
    for path, node_groups in groups_by_parent.items():
        nodes[path].groups = tuple(node_groups)

    return nodes[()], nodes


def _attach_logical_rules(
    nodes: dict[tuple[str, ...], _StructureRuleNode],
    logical_elements: tuple[LogicalStructureElement, ...],
    *,
    memo: dict[int, _StructureRuleNode],
) -> None:
    for logical in logical_elements:
        parent = nodes[logical.parent]
        kind = logical.fragment._root.kind
        parent.logical_children[kind] = _LogicalStructureRule(
            element=logical,
            root=_build_fragment_rule_tree(logical, memo=memo),
        )


def _attach_recursive_rules(
    nodes: dict[tuple[str, ...], _StructureRuleNode],
    recursive_elements: tuple[object, ...],
    *,
    owner_fragment: StructureFragment | None,
    memo: dict[int, _StructureRuleNode],
) -> None:
    for recursive in recursive_elements:
        template = recursive.template or owner_fragment
        if template is None:
            raise RuntimeError("recursive structure rule has no fragment template")
        logical = LogicalStructureElement(
            parent=recursive.parent,
            logical_name=recursive.logical_name,
            fragment=template,
            names=recursive.names,
            min_count=0,
            max_count=recursive.max_count,
        )
        parent = nodes[recursive.parent]
        parent.logical_children[template._root.kind] = _LogicalStructureRule(
            element=logical,
            root=_build_fragment_tree(template, memo=memo),
        )


def _append_binding(
    bindings: list[StructureBinding],
    logical: LogicalStructureElement,
    actual_path: tuple[str, ...],
) -> None:
    if any(
        binding.logical_element is logical and binding.actual_path == actual_path
        for binding in bindings
    ):
        return
    bindings.append(
        StructureBinding(logical_element=logical, actual_path=actual_path)
    )


def _resolve_rule_path(
    root: _StructureRuleNode,
    placement: tuple[str, ...],
    bindings: list[StructureBinding],
    *,
    focus_kind: StructuralKind,
) -> tuple[_StructureRuleNode | None, bool]:
    def walk(
        node: _StructureRuleNode,
        index: int,
        prefix: tuple[str, ...],
        collected: list[StructureBinding],
    ) -> tuple[_StructureRuleNode | None, bool, list[StructureBinding]] | None:
        if index == len(placement):
            return node, False, collected
        if node.unconstrained:
            return None, True, collected

        part = placement[index]
        next_prefix = prefix + (part,)
        exact = node.exact_children.get(part)
        if exact is not None:
            return walk(exact, index + 1, next_prefix, collected)

        candidates = [
            logical
            for logical in node.logical_children.values()
            if logical.element._accepts_name(part)
        ]
        if not candidates:
            return None

        if len(candidates) > 1 and index == len(placement) - 1:
            kind_matches = [
                logical for logical in candidates if logical.root.kind is focus_kind
            ]
            if len(kind_matches) == 1:
                candidates = kind_matches

        successful: list[tuple[_StructureRuleNode | None, bool, list[StructureBinding]]] = []
        for logical in candidates:
            branch_bindings = list(collected)
            if not any(
                binding.logical_element is logical.element
                and binding.actual_path == next_prefix
                for binding in branch_bindings
            ):
                branch_bindings.append(
                    StructureBinding(
                        logical_element=logical.element,
                        actual_path=next_prefix,
                    )
                )
            resolved = walk(
                logical.root,
                index + 1,
                next_prefix,
                branch_bindings,
            )
            if resolved is not None:
                successful.append(resolved)

        if len(successful) != 1:
            return None
        return successful[0]

    resolved = walk(root, 0, (), [])
    if resolved is None:
        return None, False
    node, below_unconstrained, resolved_bindings = resolved
    for binding in resolved_bindings:
        _append_binding(bindings, binding.logical_element, binding.actual_path)
    return node, below_unconstrained

def _actual_structure_maps(
    structure: ResolvedStructure,
    root_path: tuple[str, ...],
    placement: tuple[str, ...],
) -> tuple[
    dict[tuple[str, ...], object],
    dict[tuple[str, ...], StructuralKind],
    dict[tuple[str, ...], list[tuple[str, ...]]],
]:
    actual_by_path: dict[tuple[str, ...], object] = {}
    actual_kind_by_path: dict[tuple[str, ...], StructuralKind] = {}
    children_by_parent: dict[tuple[str, ...], list[tuple[str, ...]]] = {}
    for node in structure.nodes:
        if node.path[: len(root_path)] != root_path:
            raise ValueError("resolved structure contains a node outside its focus root")
        relative = node.path[len(root_path) :]
        effective = placement + relative
        if effective in actual_kind_by_path:
            raise ValueError(
                "resolved structure contains duplicate path: "
                f"{StructureSpecification.format_path(effective)}"
            )
        actual_by_path[effective] = node.subject
        actual_kind_by_path[effective] = node.kind
        if effective != placement:
            children_by_parent.setdefault(effective[:-1], []).append(effective)
    return actual_by_path, actual_kind_by_path, children_by_parent


def _check_exact_structure(
    structure: ResolvedStructure,
    specification: StructureSpecification,
    *,
    root_path: tuple[str, ...],
    placement: tuple[str, ...],
) -> StructureCheck:
    expected_root = specification.element_at(placement)
    if expected_root is None:
        diagnostic = Diagnostic(
            "structure placement is not defined by the specification: "
            f"{StructureSpecification.format_path(placement)}",
            code="structure.placement.undefined",
            subject=structure.focus.subject,
        )
        return StructureCheck(
            specification=specification,
            placement=placement,
            diagnostics=(diagnostic,),
        )

    actual_by_path, actual_kind_by_path, _ = _actual_structure_maps(
        structure,
        root_path,
        placement,
    )
    expected = {
        element.path: element.kind for element in specification.subtree(placement)
    }
    diagnostics: list[Diagnostic] = []

    for path, expected_kind in expected.items():
        actual_kind = actual_kind_by_path.get(path)
        if actual_kind is None:
            diagnostics.append(
                Diagnostic(
                    "required structural element is missing: "
                    f"{StructureSpecification.format_path(path)} "
                    f"({expected_kind.value})",
                    code="structure.element.missing",
                    subject=structure.focus.subject,
                )
            )
            continue
        if actual_kind is not expected_kind:
            diagnostics.append(
                Diagnostic(
                    "structural kind does not match at "
                    f"{StructureSpecification.format_path(path)}: expected "
                    f"{expected_kind.value}, got {actual_kind.value}",
                    code="structure.kind.mismatch",
                    subject=actual_by_path[path],
                )
            )

    for path, actual_kind in actual_kind_by_path.items():
        if path in expected:
            continue
        diagnostics.append(
            Diagnostic(
                "unexpected structural element: "
                f"{StructureSpecification.format_path(path)} ({actual_kind.value})",
                code="structure.element.unexpected",
                subject=actual_by_path[path],
            )
        )

    return StructureCheck(
        specification=specification,
        placement=placement,
        diagnostics=tuple(diagnostics),
    )


def _emit_missing_rule(
    rule: _StructureRuleNode,
    path: tuple[str, ...],
    *,
    subject: object,
    diagnostics: list[Diagnostic],
) -> None:
    if not rule.required:
        return
    diagnostics.append(
        Diagnostic(
            "required structural element is missing: "
            f"{StructureSpecification.format_path(path)} ({rule.kind.value})",
            code="structure.element.missing",
            subject=subject,
        )
    )
    if rule.unconstrained:
        return
    for name, child in rule.exact_children.items():
        _emit_missing_rule(
            child,
            path + (name,),
            subject=subject,
            diagnostics=diagnostics,
        )


def _emit_unexpected_subtree(
    path: tuple[str, ...],
    *,
    actual_by_path: dict[tuple[str, ...], object],
    actual_kind_by_path: dict[tuple[str, ...], StructuralKind],
    children_by_parent: dict[tuple[str, ...], list[tuple[str, ...]]],
    diagnostics: list[Diagnostic],
) -> None:
    diagnostics.append(
        Diagnostic(
            "unexpected structural element: "
            f"{StructureSpecification.format_path(path)} "
            f"({actual_kind_by_path[path].value})",
            code="structure.element.unexpected",
            subject=actual_by_path[path],
        )
    )
    for child in children_by_parent.get(path, ()):  # preserve observed order
        _emit_unexpected_subtree(
            child,
            actual_by_path=actual_by_path,
            actual_kind_by_path=actual_kind_by_path,
            children_by_parent=children_by_parent,
            diagnostics=diagnostics,
        )


def _match_dynamic_rule(
    rule: _StructureRuleNode,
    path: tuple[str, ...],
    *,
    actual_by_path: dict[tuple[str, ...], object],
    actual_kind_by_path: dict[tuple[str, ...], StructuralKind],
    children_by_parent: dict[tuple[str, ...], list[tuple[str, ...]]],
    diagnostics: list[Diagnostic],
    bindings: list[StructureBinding],
) -> None:
    actual_kind = actual_kind_by_path[path]
    if actual_kind is not rule.kind:
        diagnostics.append(
            Diagnostic(
                "structural kind does not match at "
                f"{StructureSpecification.format_path(path)}: expected "
                f"{rule.kind.value}, got {actual_kind.value}",
                code="structure.kind.mismatch",
                subject=actual_by_path[path],
            )
        )

    if rule.unconstrained:
        return

    actual_children = children_by_parent.get(path, ())
    actual_children_by_name = {child[-1]: child for child in actual_children}
    consumed: set[tuple[str, ...]] = set()

    for name, child_rule in rule.exact_children.items():
        child_path = actual_children_by_name.get(name)
        if child_path is None:
            _emit_missing_rule(
                child_rule,
                path + (name,),
                subject=actual_by_path[path],
                diagnostics=diagnostics,
            )
            continue
        consumed.add(child_path)
        _match_dynamic_rule(
            child_rule,
            child_path,
            actual_by_path=actual_by_path,
            actual_kind_by_path=actual_kind_by_path,
            children_by_parent=children_by_parent,
            diagnostics=diagnostics,
            bindings=bindings,
        )

    for group in rule.groups:
        count = sum(name in actual_children_by_name for name in group.members)
        if count < group.min_count:
            diagnostics.append(
                Diagnostic(
                    f"structure group {group.members!r} requires at least "
                    f"{group.min_count} member(s) under "
                    f"{StructureSpecification.format_path(path)}; got {count}",
                    code="structure.group.minimum",
                    subject=actual_by_path[path],
                )
            )
        if group.max_count is not None and count > group.max_count:
            diagnostics.append(
                Diagnostic(
                    f"structure group {group.members!r} allows at most "
                    f"{group.max_count} member(s) under "
                    f"{StructureSpecification.format_path(path)}; got {count}",
                    code="structure.group.maximum",
                    subject=actual_by_path[path],
                )
            )

    logical_matches: dict[int, list[tuple[str, ...]]] = {
        id(logical): [] for logical in rule.logical_children.values()
    }
    for child_path in actual_children:
        if child_path in consumed:
            continue
        child_kind = actual_kind_by_path[child_path]
        logical = rule.logical_children.get(child_kind)
        if logical is not None and not logical.element._accepts_name(child_path[-1]):
            logical = None
        if logical is None:
            candidates = [
                candidate
                for candidate in rule.logical_children.values()
                if candidate.element._accepts_name(child_path[-1])
            ]
            if len(candidates) == 1:
                logical = candidates[0]
        if logical is None:
            continue
        logical_matches[id(logical)].append(child_path)
        consumed.add(child_path)
        _append_binding(bindings, logical.element, child_path)
        _match_dynamic_rule(
            logical.root,
            child_path,
            actual_by_path=actual_by_path,
            actual_kind_by_path=actual_kind_by_path,
            children_by_parent=children_by_parent,
            diagnostics=diagnostics,
            bindings=bindings,
        )

    for logical in rule.logical_children.values():
        count = len(logical_matches[id(logical)])
        if count < logical.element.min_count:
            diagnostics.append(
                Diagnostic(
                    f"logical structural element {logical.element.logical_name!r} "
                    f"requires at least {logical.element.min_count} instance(s) under "
                    f"{StructureSpecification.format_path(path)}; got {count}",
                    code="structure.logical.minimum",
                    subject=actual_by_path[path],
                )
            )
        if (
            logical.element.max_count is not None
            and count > logical.element.max_count
        ):
            diagnostics.append(
                Diagnostic(
                    f"logical structural element {logical.element.logical_name!r} "
                    f"allows at most {logical.element.max_count} instance(s) under "
                    f"{StructureSpecification.format_path(path)}; got {count}",
                    code="structure.logical.maximum",
                    subject=actual_by_path[path],
                )
            )

    for child_path in actual_children:
        if child_path in consumed:
            continue
        _emit_unexpected_subtree(
            child_path,
            actual_by_path=actual_by_path,
            actual_kind_by_path=actual_kind_by_path,
            children_by_parent=children_by_parent,
            diagnostics=diagnostics,
        )


def _check_dynamic_structure(
    structure: ResolvedStructure,
    specification: StructureSpecification,
    *,
    root_path: tuple[str, ...],
    placement: tuple[str, ...],
) -> StructureCheck:
    rule_root = _build_rule_tree(specification)
    bindings: list[StructureBinding] = []
    placement_rule, below_unconstrained = _resolve_rule_path(
        rule_root,
        placement,
        bindings,
        focus_kind=next(
            node.kind for node in structure.nodes if node.subject is structure.focus.subject
        ),
    )
    if placement_rule is None and not below_unconstrained:
        diagnostic = Diagnostic(
            "structure placement is not defined by the specification: "
            f"{StructureSpecification.format_path(placement)}",
            code="structure.placement.undefined",
            subject=structure.focus.subject,
        )
        return StructureCheck(
            specification=specification,
            placement=placement,
            diagnostics=(diagnostic,),
            bindings=tuple(bindings),
        )

    if below_unconstrained:
        return StructureCheck(
            specification=specification,
            placement=placement,
            diagnostics=(),
            bindings=tuple(bindings),
        )

    actual_by_path, actual_kind_by_path, children_by_parent = _actual_structure_maps(
        structure,
        root_path,
        placement,
    )
    diagnostics: list[Diagnostic] = []
    if placement not in actual_kind_by_path:
        raise ValueError("resolved structure has no effective focus root")

    _match_dynamic_rule(
        placement_rule,
        placement,
        actual_by_path=actual_by_path,
        actual_kind_by_path=actual_kind_by_path,
        children_by_parent=children_by_parent,
        diagnostics=diagnostics,
        bindings=bindings,
    )
    return StructureCheck(
        specification=specification,
        placement=placement,
        diagnostics=tuple(diagnostics),
        bindings=tuple(bindings),
    )


def check_structure(
    structure: ResolvedStructure,
    specification: StructureSpecification,
) -> StructureCheck:
    """Check one resolved focus against the matching specification subtree.

    Required exact-only specifications retain the original closed-subtree
    comparison. Optional exact elements activate only when their parent
    regulation is active and the concrete element exists. Specifications with
    logical elements resolve concrete names by structural position: an explicit
    exact child wins, otherwise the parent's single logical element may bind the
    concrete child. Unconstrained fragments make the selected subtree explicitly
    open instead of changing exact semantics.
    """

    root = structure.node_for(structure.focus.subject)
    if root is None:  # defensive; ResolvedStructure already guarantees this
        raise ValueError("resolved structure has no focus node")

    placement = structure.focus.placement or ()
    if (
        not specification.logical_elements
        and not specification._recursive_elements
        and not specification.groups
        and not specification._unconstrained_paths
        and all(element.required for element in specification.elements)
    ):
        return _check_exact_structure(
            structure,
            specification,
            root_path=root.path,
            placement=placement,
        )
    return _check_dynamic_structure(
        structure,
        specification,
        root_path=root.path,
        placement=placement,
    )


def validator(
    *,
    focus: StructuralKind,
    name: str | None = None,
) -> Callable[[ValidationFunction], ValidationRule]:
    """Create a validation rule from a function.

    The decorated function receives a :class:`SemanticView` centered on the
    declared structural kind and returns or yields :class:`Diagnostic` objects.
    """

    def decorate(function: ValidationFunction) -> ValidationRule:
        rule_name = name if name is not None else function.__name__
        if not rule_name:
            raise ValueError("validation rule name must not be empty")
        return ValidationRule(
            focus_kind=focus,
            check=function,
            name=rule_name,
        )

    return decorate
