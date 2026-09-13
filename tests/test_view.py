from __future__ import annotations

import types

import pytest

from shikumi import (
    InformationType,
    Shikumi,
    StructuralKind,
    UnknownViewSubjectError,
    attach_information,
    clear_information,
)


def test_module_view_exposes_focus_entities_and_information() -> None:
    title = InformationType("title", str)
    module = types.ModuleType("docs.auth")
    exec(
        compile(
            "class Login: pass\nclass RefreshToken: pass",
            "<docs.auth>",
            "exec",
        ),
        module.__dict__,
    )
    login = module.Login
    refresh = module.RefreshToken

    try:
        attach_information(module, title, "Authentication")
        attach_information(login, title, "Login")
        attach_information(refresh, title, "Refresh token")

        view = Shikumi(information_types=[title]).view(module)

        assert view.focused.subject is module
        assert view.focused.kind is StructuralKind.MODULE
        assert view.focused.values(title) == ("Authentication",)
        assert tuple(item.subject for item in view.entities) == (login, refresh)
        assert view.item(login).values(title) == ("Login",)
        assert view.item(refresh).values(title) == ("Refresh token",)
    finally:
        clear_information(module)
        clear_information(login)
        clear_information(refresh)


def test_class_information_does_not_leak_through_inheritance() -> None:
    title = InformationType("title", str)

    class Base:
        pass

    class Child(Base):
        pass

    try:
        attach_information(Base, title, "Base")

        shikumi = Shikumi(information_types=[title])

        assert shikumi.view(Base).focused.values(title) == ("Base",)
        assert shikumi.view(Child).focused.values(title) == ()
    finally:
        clear_information(Base)
        clear_information(Child)


def test_view_item_lookup_is_identity_based() -> None:
    module = types.ModuleType("docs.identity")
    exec(compile("class Page: pass", "<docs.identity>", "exec"), module.__dict__)

    view = Shikumi().view(module)

    assert view.item(module.Page).subject is module.Page
    with pytest.raises(UnknownViewSubjectError):
        view.item(type("Page", (), {}))


def test_shikumi_rejects_duplicate_information_type_objects() -> None:
    title = InformationType("title", str)

    with pytest.raises(ValueError):
        Shikumi(information_types=[title, title])


def test_semantic_view_subview_reuses_already_interpreted_records() -> None:
    title = InformationType("title", str)
    module = types.ModuleType("docs.subview")
    exec(compile("class Outer:\n    class Inner: pass", "<docs.subview>", "exec"), module.__dict__)

    try:
        attach_information(module.Outer, title, "Outer")
        attach_information(module.Outer.Inner, title, "Inner")
        view = Shikumi(information_types=[title]).view(module)

        assert view.subview(module) is view

        subview = view.subview(module.Outer)

        assert subview.focus.subject is module.Outer
        assert subview.focus.placement == view.item(module.Outer).node.path
        assert tuple(item.subject for item in subview.items) == (
            module.Outer,
            module.Outer.Inner,
        )
        assert subview.item(module.Outer).information is view.item(module.Outer).information
        assert subview.item(module.Outer.Inner).information is view.item(module.Outer.Inner).information
    finally:
        clear_information(module.Outer)
        clear_information(module.Outer.Inner)
