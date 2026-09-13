from __future__ import annotations

import types

from shikumi import (
    Diagnostic,
    InformationType,
    RealizationCheck,
    Realizer,
    SemanticView,
    Shikumi,
    attach_information,
    clear_information,
)


class TitlesRealizer(Realizer[tuple[str, ...]]):
    def __init__(self, title: InformationType) -> None:
        self.title = title

    def realize(self, view: SemanticView) -> tuple[str, ...]:
        return tuple(
            value
            for item in view.items
            for value in item.values(self.title)
            if isinstance(value, str)
        )


class PathsRealizer(Realizer[tuple[tuple[str, ...], ...]]):
    def realize(self, view: SemanticView) -> tuple[tuple[str, ...], ...]:
        return tuple(item.node.path for item in view.items)


def test_realizer_consumes_an_existing_semantic_view() -> None:
    title = InformationType("title", str)

    class Page:
        pass

    try:
        attach_information(Page, title, "Overview")
        view = Shikumi(information_types=[title]).view(Page)

        artifact = TitlesRealizer(title).realize(view)

        assert artifact == ("Overview",)
    finally:
        clear_information(Page)


def test_multiple_realizers_can_consume_the_same_view() -> None:
    title = InformationType("title", str)
    module = types.ModuleType("docs.pages")
    exec(compile("class Page: pass", "<docs.pages>", "exec"), module.__dict__)

    try:
        attach_information(module.Page, title, "Overview")
        view = Shikumi(information_types=[title]).view(module)

        assert TitlesRealizer(title).realize(view) == ("Overview",)
        assert PathsRealizer().realize(view) == (
            ("docs", "pages"),
            ("docs", "pages", "Page"),
        )
    finally:
        clear_information(module.Page)


def test_realizer_may_return_any_python_artifact_type() -> None:
    class MappingRealizer(Realizer[dict[str, int]]):
        def realize(self, view: SemanticView) -> dict[str, int]:
            return {"items": len(view.items)}

    class Page:
        pass

    view = Shikumi().view(Page)

    assert MappingRealizer().realize(view) == {"items": 1}


def test_shikumi_does_not_own_or_select_a_realizer() -> None:
    class Page:
        pass

    shikumi = Shikumi()
    view = shikumi.view(Page)

    assert PathsRealizer().realize(view) == (view.focused.node.path,)
    assert not hasattr(shikumi, "realizer")
    assert not hasattr(shikumi, "realize")


def test_realizer_check_can_report_realizability_without_realizing() -> None:
    calls: list[str] = []

    class StrictRealizer(Realizer[str]):
        def check(self, view: SemanticView) -> RealizationCheck:
            calls.append("check")
            return RealizationCheck(
                view,
                (Diagnostic("required information is missing", code="realizer.required"),),
            )

        def realize(self, view: SemanticView) -> str:
            calls.append("realize")
            return "artifact"

    class Page:
        pass

    view = Shikumi().view(Page)
    result = StrictRealizer().check(view)

    assert not result.is_realizable
    assert result.diagnostics[0].code == "realizer.required"
    assert result.diagnostics[0].subject is Page
    assert calls == ["check"]


def test_realizer_default_check_declares_no_additional_preconditions() -> None:
    class AnyViewRealizer(Realizer[str]):
        def realize(self, view: SemanticView) -> str:
            return "ok"

    class Page:
        pass

    view = Shikumi().view(Page)

    assert AnyViewRealizer().check(view).is_realizable
