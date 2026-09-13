from __future__ import annotations

import importlib
import sys

from shikumi import (
    Diagnostic,
    InformationType,
    Realizer,
    Shikumi,
    StructuralKind,
    clear_information,
    validator,
)
from shikumi.standard import PackageTreeStructure, assignment, information_type_rule


def _defined_class(source: str, **names: object) -> type[object]:
    namespace: dict[str, object] = {"__name__": "tests.integration", **names}
    exec(compile(source, "<integration-test>", "exec"), namespace)
    return namespace["Page"]  # type: ignore[return-value]


def test_core_flow_from_description_through_validation_and_realization() -> None:
    title_type = InformationType("title", str)
    title = assignment(title_type)
    Page = _defined_class(
        'class Page:\n    title @= "Overview"\n',
        title=title,
    )

    @validator(focus=StructuralKind.ENTITY)
    def require_title(view):
        if not view.focused.has(title_type):
            yield Diagnostic("title is required", code="title.required")

    class MappingRealizer(Realizer[dict[str, str]]):
        def realize(self, view):
            return {"title": view.focused.values(title_type)[0]}

    try:
        docs = Shikumi(
            information_types=[title_type],
            validators=[require_title, information_type_rule(title_type)],
        )

        view = docs.view(Page)
        result = docs.validate(Page)
        artifact = MappingRealizer().realize(view)

        assert view.focused.values(title_type) == ("Overview",)
        assert result.is_valid
        assert result.diagnostics == ()
        assert artifact == {"title": "Overview"}
    finally:
        clear_information(Page)


def test_standard_package_flow_uses_runtime_imported_information(
    tmp_path, monkeypatch
) -> None:
    root = tmp_path / "shikumi_integration_docs"
    root.mkdir()
    (root / "__init__.py").write_text(
        "\n".join(
            [
                "from shikumi.standard import content_type, docstring",
                "Content = content_type()",
                "content = docstring(Content)",
                "@content",
                "class Root:",
                '    \"\"\"Root document.\"\"\"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    (root / "guide.py").write_text(
        "\n".join(
            [
                "from . import content",
                "@content",
                "class Guide:",
                '    \"\"\"Guide document.\"\"\"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.syspath_prepend(str(tmp_path))
    package = importlib.import_module("shikumi_integration_docs")

    try:
        docs = Shikumi(
            structure=PackageTreeStructure(),
            information_types=[package.Content],
            validators=[information_type_rule(package.Content)],
        )

        view = docs.view(package)
        result = docs.validate(package)

        assert [item.node.path for item in view.entities] == [
            ("shikumi_integration_docs", "Root"),
            ("shikumi_integration_docs", "guide", "Guide"),
        ]
        assert [item.values(package.Content)[0] for item in view.entities] == [
            "Root document.",
            "Guide document.",
        ]
        assert result.is_valid
    finally:
        for item in docs.view(package).items:
            clear_information(item.subject)
        for name in tuple(sys.modules):
            if name == "shikumi_integration_docs" or name.startswith(
                "shikumi_integration_docs."
            ):
                sys.modules.pop(name, None)
