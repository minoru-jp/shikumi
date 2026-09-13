from __future__ import annotations

import types

import pytest

from shikumi import (
    Diagnostic,
    DiagnosticSeverity,
    InformationType,
    Focus,
    PythonStructure,
    Shikumi,
    StructuralKind,
    Structure,
    ValidationRule,
    attach_information,
    clear_information,
    validator,
)


def _module(name: str, source: str) -> types.ModuleType:
    module = types.ModuleType(name)
    exec(compile(source, f"<{name}>", "exec"), module.__dict__)
    return module


def test_entity_focus_can_be_validated_directly() -> None:
    title = InformationType("title", str)

    @validator(focus=StructuralKind.ENTITY)
    def require_title(view):
        if not view.focused.has(title):
            yield Diagnostic("title is required", code="title.required")

    class Page:
        pass

    result = Shikumi(
        information_types=[title],
        validators=[require_title],
    ).validate(Page)

    assert not result.is_valid
    assert len(result.diagnostics) == 1
    assert result.diagnostics[0].code == "title.required"
    assert result.diagnostics[0].subject is Page


def test_module_validation_applies_entity_rules_to_entities_in_the_view() -> None:
    title = InformationType("title", str)
    module = _module("docs.pages", "class First: pass\nclass Second: pass")

    @validator(focus=StructuralKind.ENTITY)
    def require_title(view):
        if not view.focused.has(title):
            yield Diagnostic("title is required")

    try:
        attach_information(module.First, title, "First")
        result = Shikumi(
            information_types=[title],
            validators=[require_title],
        ).validate(module, placement=("docs", "pages"))

        assert not result.is_valid
        assert tuple(item.subject for item in result.view.entities) == (
            module.First,
            module.Second,
        )
        assert tuple(item.subject for item in result.diagnostics) == (module.Second,)
    finally:
        clear_information(module.First)
        clear_information(module.Second)


def test_module_and_entity_rules_share_one_validation_operation() -> None:
    module = _module("docs.shared", "class Page: pass")
    calls: list[tuple[str, object]] = []

    @validator(focus=StructuralKind.MODULE)
    def module_rule(view):
        calls.append(("module", view.focus.subject))

    @validator(focus=StructuralKind.ENTITY)
    def entity_rule(view):
        calls.append(("entity", view.focus.subject))

    result = Shikumi(validators=[module_rule, entity_rule]).validate(module, placement=("docs", "shared"))

    assert result.is_valid
    assert calls == [
        ("module", module),
        ("entity", module.Page),
    ]


def test_entity_validation_does_not_synthesize_a_module_focus() -> None:
    calls: list[str] = []

    @validator(focus=StructuralKind.MODULE)
    def module_rule(view):
        calls.append("module")

    @validator(focus=StructuralKind.ENTITY)
    def entity_rule(view):
        calls.append("entity")

    class Page:
        pass

    Shikumi(validators=[module_rule, entity_rule]).validate(Page)

    assert calls == ["entity"]


def test_explicit_diagnostic_subject_is_preserved() -> None:
    module = _module("docs.explicit", "class Page: pass")

    @validator(focus=StructuralKind.MODULE)
    def rule(view):
        yield Diagnostic("page problem", subject=module.Page)

    result = Shikumi(validators=[rule]).validate(module, placement=("docs", "explicit"))

    assert result.diagnostics[0].subject is module.Page


def test_warning_does_not_make_validation_invalid() -> None:
    @validator(focus=StructuralKind.ENTITY)
    def warning_rule(view):
        return Diagnostic(
            "optional information is missing",
            severity=DiagnosticSeverity.WARNING,
        )

    class Page:
        pass

    result = Shikumi(validators=[warning_rule]).validate(Page)

    assert result.is_valid
    assert bool(result)


def test_rule_rejects_a_view_with_the_wrong_focus_kind() -> None:
    rule = ValidationRule(
        focus_kind=StructuralKind.MODULE,
        check=lambda view: None,
        name="module_only",
    )

    class Page:
        pass

    view = Shikumi().view(Page)

    with pytest.raises(ValueError, match="requires focus kind"):
        rule(view)


def test_rules_must_produce_diagnostics() -> None:
    @validator(focus=StructuralKind.ENTITY)
    def bad_rule(view):
        return ["not a diagnostic"]

    class Page:
        pass

    with pytest.raises(TypeError, match="Diagnostic"):
        Shikumi(validators=[bad_rule]).validate(Page)


def test_duplicate_validation_rule_objects_are_rejected() -> None:
    @validator(focus=StructuralKind.ENTITY)
    def rule(view):
        return None

    with pytest.raises(ValueError, match="validators"):
        Shikumi(validators=[rule, rule])


def test_module_validation_exposes_the_explicit_planned_placement() -> None:
    module = _module("temporary.generated", "class Page: pass")
    observed: list[tuple[str, ...]] = []

    @validator(focus=StructuralKind.MODULE)
    def module_path(view):
        observed.append(view.focused.node.path)

    result = Shikumi(validators=[module_path]).validate(
        module,
        placement=("docs", "pages"),
    )

    assert result.is_valid
    assert observed == [("docs", "pages")]


def test_diagnostic_rejects_invalid_constructor_values() -> None:
    with pytest.raises(TypeError, match="message must be a string"):
        Diagnostic(1)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="code must be a string or None"):
        Diagnostic("problem", code=1)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="severity must be a DiagnosticSeverity"):
        Diagnostic("problem", severity="error")  # type: ignore[arg-type]


def test_validation_rule_rejects_invalid_constructor_values() -> None:
    with pytest.raises(TypeError, match="focus_kind must be a StructuralKind"):
        ValidationRule(  # type: ignore[arg-type]
            focus_kind="entity",
            check=lambda view: None,
            name="rule",
        )
    with pytest.raises(TypeError, match="check must be callable"):
        ValidationRule(  # type: ignore[arg-type]
            focus_kind=StructuralKind.ENTITY,
            check=None,
            name="rule",
        )
    with pytest.raises(TypeError, match="name must be a string"):
        ValidationRule(  # type: ignore[arg-type]
            focus_kind=StructuralKind.ENTITY,
            check=lambda view: None,
            name=1,
        )
    with pytest.raises(ValueError, match="name must not be empty"):
        ValidationRule(
            focus_kind=StructuralKind.ENTITY,
            check=lambda view: None,
            name="",
        )


def test_validation_resolves_structure_once_for_all_rules() -> None:
    module = _module("docs.once", "class First: pass\nclass Second: pass")

    class CountingStructure(Structure):
        def __init__(self) -> None:
            self.calls = 0
            self.delegate = PythonStructure()

        def resolve(self, focus: Focus):
            self.calls += 1
            return self.delegate.resolve(focus)

    structure = CountingStructure()

    @validator(focus=StructuralKind.MODULE)
    def module_rule(view):
        assert view.focus.subject is module

    @validator(focus=StructuralKind.ENTITY)
    def entity_rule(view):
        assert view.focus.subject in (module.First, module.Second)

    result = Shikumi(
        structure=structure,
        validators=[module_rule, entity_rule],
    ).validate(module, placement=("docs", "once"))

    assert result.is_valid
    assert structure.calls == 1
