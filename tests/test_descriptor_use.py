from __future__ import annotations

import types

import pytest

from shikumi import (
    DescriptorUseRule,
    DiagnosticSeverity,
    Shikumi,
    StructuralKind,
    StructureSelector,
    clear_descriptor_uses,
    descriptor_uses_of,
    record_descriptor_use,
)


def _module(name: str, source: str) -> types.ModuleType:
    module = types.ModuleType(name)
    exec(compile(source, f"<{name}>", "exec"), module.__dict__)  # noqa: S102 - trusted in-test source is executed intentionally
    return module


def test_descriptor_use_is_recorded_independently_of_information() -> None:
    descriptor = object()

    class Page:
        pass

    try:
        use = record_descriptor_use(Page, descriptor)

        assert use.subject is Page
        assert use.descriptor is descriptor
        assert descriptor_uses_of(Page) == (use,)
        assert Shikumi().view(Page).focused.descriptor_uses == (use,)
        assert Shikumi().view(Page).focused.uses(descriptor) == (use,)
    finally:
        clear_descriptor_uses(Page)


def test_bound_method_descriptor_matches_repeated_attribute_access() -> None:
    class Writer:
        def describe(self, subject: object) -> None:
            record_descriptor_use(subject, self.describe)

    writer = Writer()

    class Page:
        pass

    try:
        writer.describe(Page)
        view = Shikumi().view(Page)

        assert len(view.focused.uses(writer.describe)) == 1
    finally:
        clear_descriptor_uses(Page)


def test_unregulated_descriptor_use_is_allowed() -> None:
    descriptor = object()

    class Page:
        pass

    try:
        record_descriptor_use(Page, descriptor)
        result = Shikumi().validate(Page)

        assert result.is_valid
        assert result.diagnostics == ()
    finally:
        clear_descriptor_uses(Page)


def test_disallowed_descriptor_use_is_an_error() -> None:
    descriptor = object()

    class Page:
        pass

    try:
        record_descriptor_use(Page, descriptor)
        rule = DescriptorUseRule(
            descriptor=descriptor,
            allowed=StructureSelector(kind=StructuralKind.MODULE),
            name="module-only",
        )
        result = Shikumi(descriptor_rules=[rule]).validate(Page)

        assert not result.is_valid
        assert len(result.diagnostics) == 1
        diagnostic = result.diagnostics[0]
        assert diagnostic.code == "descriptor.use.disallowed"
        assert diagnostic.severity is DiagnosticSeverity.ERROR
        assert diagnostic.subject is Page
    finally:
        clear_descriptor_uses(Page)


def test_allowed_but_not_recommended_descriptor_use_is_a_warning() -> None:
    descriptor = object()
    module = _module("temporary.users", "class GetUser: pass")

    try:
        record_descriptor_use(module.GetUser, descriptor)
        rule = DescriptorUseRule(
            descriptor=descriptor,
            allowed=StructureSelector(kind=StructuralKind.ENTITY),
            recommended=StructureSelector(
                kind=StructuralKind.ENTITY,
                under=("public",),
            ),
            name="endpoint",
        )
        result = Shikumi(descriptor_rules=[rule]).validate(
            module,
            placement=("users",),
        )

        assert result.is_valid
        assert len(result.diagnostics) == 1
        diagnostic = result.diagnostics[0]
        assert diagnostic.code == "descriptor.use.not_recommended"
        assert diagnostic.severity is DiagnosticSeverity.WARNING
        assert diagnostic.subject is module.GetUser
    finally:
        clear_descriptor_uses(module.GetUser)


def test_descriptor_rule_uses_planned_module_placement() -> None:
    descriptor = object()
    module = _module("temporary.generated", "class GetUser: pass")

    try:
        record_descriptor_use(module.GetUser, descriptor)
        rule = DescriptorUseRule(
            descriptor=descriptor,
            allowed=StructureSelector(
                kind=StructuralKind.ENTITY,
                under=("api",),
            ),
        )

        allowed = Shikumi(descriptor_rules=[rule]).validate(
            module,
            placement=("api", "users"),
        )
        disallowed = Shikumi(descriptor_rules=[rule]).validate(
            module,
            placement=("internal", "users"),
        )

        assert allowed.is_valid
        assert allowed.diagnostics == ()
        assert not disallowed.is_valid
        assert disallowed.diagnostics[0].code == "descriptor.use.disallowed"
    finally:
        clear_descriptor_uses(module.GetUser)


def test_structure_selector_at_is_exact_and_under_is_inclusive() -> None:
    entity = StructuralKind.ENTITY

    assert StructureSelector(kind=entity, at=("api", "users")).matches(
        kind=entity,
        path=("api", "users"),
    )
    assert not StructureSelector(kind=entity, at=("api", "users")).matches(
        kind=entity,
        path=("api", "users", "GetUser"),
    )
    under = StructureSelector(under=("api",))
    assert under.matches(kind=StructuralKind.MODULE, path=("api",))
    assert under.matches(kind=entity, path=("api", "users", "GetUser"))
    assert not under.matches(kind=entity, path=("internal", "GetUser"))


def test_structure_selector_rejects_ambiguous_path_constraints() -> None:
    with pytest.raises(ValueError, match="both at and under"):
        StructureSelector(at=("api",), under=("api",))


def test_duplicate_descriptor_rule_object_is_rejected() -> None:
    rule = DescriptorUseRule(
        descriptor=object(),
        allowed=StructureSelector(),
    )

    with pytest.raises(ValueError, match="descriptor_rules"):
        Shikumi(descriptor_rules=[rule, rule])


def test_structure_selectors_can_express_alternative_locations() -> None:
    selector = StructureSelector(kind=StructuralKind.MODULE) | StructureSelector(
        kind=StructuralKind.ENTITY, under=("api",)
    )

    assert selector.matches(kind=StructuralKind.MODULE, path=("internal",))
    assert selector.matches(kind=StructuralKind.ENTITY, path=("api", "GetUser"))
    assert not selector.matches(
        kind=StructuralKind.ENTITY,
        path=("internal", "Worker"),
    )


def test_descriptor_use_registry_is_identity_based_even_for_equal_subjects() -> None:
    class EqualSubject:
        def __init__(self, key: str) -> None:
            self.key = key

        def __eq__(self, other: object) -> bool:
            return isinstance(other, EqualSubject) and self.key == other.key

        def __hash__(self) -> int:
            return hash(self.key)

    left_descriptor = object()
    right_descriptor = object()
    left = EqualSubject("same")
    right = EqualSubject("same")

    try:
        record_descriptor_use(left, left_descriptor)
        record_descriptor_use(right, right_descriptor)

        assert descriptor_uses_of(left)[0].descriptor is left_descriptor
        assert descriptor_uses_of(right)[0].descriptor is right_descriptor
        assert descriptor_uses_of(left)[0].subject is left
        assert descriptor_uses_of(right)[0].subject is right
    finally:
        clear_descriptor_uses(left)
        clear_descriptor_uses(right)


def test_descriptor_use_registry_does_not_keep_subject_alive() -> None:
    import gc
    import weakref

    descriptor = object()

    def record_temporary_subject():
        class Temporary:
            pass

        subject_ref = weakref.ref(Temporary)
        record_descriptor_use(Temporary, descriptor)
        return subject_ref

    subject_ref = record_temporary_subject()
    gc.collect()

    assert subject_ref() is None
