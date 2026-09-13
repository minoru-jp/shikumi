from __future__ import annotations

import importlib
import sys

from shikumi import Focus, Shikumi, StructuralKind
from shikumi.standard import PackageTreeStructure


def test_package_tree_structure_imports_and_resolves_physical_children(
    tmp_path, monkeypatch
) -> None:
    root = tmp_path / "docs_tree_example"
    root.mkdir()
    (root / "__init__.py").write_text("class Root: pass\n", encoding="utf-8")
    (root / "guide.py").write_text(
        "class Guide:\n    class Section:\n        pass\n",
        encoding="utf-8",
    )
    api = root / "api"
    api.mkdir()
    (api / "__init__.py").write_text("class ApiRoot: pass\n", encoding="utf-8")
    (api / "users.py").write_text("class User: pass\n", encoding="utf-8")

    monkeypatch.syspath_prepend(str(tmp_path))
    package = importlib.import_module("docs_tree_example")

    try:
        view = Shikumi(structure=PackageTreeStructure()).view(package)

        assert [(item.kind, item.node.path) for item in view.items] == [
            (StructuralKind.PACKAGE, ("docs_tree_example",)),
            (StructuralKind.ENTITY, ("docs_tree_example", "Root")),
            (StructuralKind.PACKAGE, ("docs_tree_example", "api")),
            (StructuralKind.ENTITY, ("docs_tree_example", "api", "ApiRoot")),
            (StructuralKind.MODULE, ("docs_tree_example", "api", "users")),
            (StructuralKind.ENTITY, ("docs_tree_example", "api", "users", "User")),
            (StructuralKind.MODULE, ("docs_tree_example", "guide")),
            (StructuralKind.ENTITY, ("docs_tree_example", "guide", "Guide")),
            (
                StructuralKind.ENTITY,
                ("docs_tree_example", "guide", "Guide", "Section"),
            ),
        ]

        api_module = sys.modules["docs_tree_example.api"]
        users_module = sys.modules["docs_tree_example.api.users"]
        guide_module = sys.modules["docs_tree_example.guide"]

        assert view.item(api_module).node.parent is package
        assert view.item(users_module).node.parent is api_module
        assert view.item(guide_module).node.parent is package
        assert view.item(users_module.User).node.parent is users_module
        assert view.item(guide_module.Guide.Section).node.parent is guide_module.Guide
    finally:
        for name in tuple(sys.modules):
            if name == "docs_tree_example" or name.startswith("docs_tree_example."):
                sys.modules.pop(name, None)


def test_package_tree_structure_keeps_single_module_focus_non_recursive(
    tmp_path, monkeypatch
) -> None:
    root = tmp_path / "docs_tree_module_focus"
    root.mkdir()
    (root / "__init__.py").write_text("", encoding="utf-8")
    (root / "page.py").write_text("class Page: pass\n", encoding="utf-8")

    monkeypatch.syspath_prepend(str(tmp_path))
    module = importlib.import_module("docs_tree_module_focus.page")

    try:
        resolved = PackageTreeStructure().resolve(Focus(module))
        assert [node.kind for node in resolved.nodes] == [
            StructuralKind.MODULE,
            StructuralKind.ENTITY,
        ]
    finally:
        for name in tuple(sys.modules):
            if name == "docs_tree_module_focus" or name.startswith(
                "docs_tree_module_focus."
            ):
                sys.modules.pop(name, None)


def test_descriptor_selector_paths_are_package_root_relative(tmp_path, monkeypatch) -> None:
    import sys
    import types

    from shikumi import DescriptorUseRule, InformationType, StructureSelector
    from shikumi.standard import assignment

    marker_type = InformationType("marker", str)
    marker = assignment(marker_type)
    fixture = types.ModuleType("shikumi_descriptor_fixture")
    fixture.marker = marker
    sys.modules[fixture.__name__] = fixture

    root = tmp_path / "descriptor_path_package"
    root.mkdir()
    (root / "__init__.py").write_text("", encoding="utf-8")
    (root / "api.py").write_text(
        "from shikumi_descriptor_fixture import marker\n"
        "class Endpoint:\n"
        "    marker @= 'yes'\n",
        encoding="utf-8",
    )

    monkeypatch.syspath_prepend(str(tmp_path))
    package = importlib.import_module("descriptor_path_package")

    try:
        rule = DescriptorUseRule(
            descriptor=marker,
            allowed=StructureSelector(
                kind=StructuralKind.ENTITY,
                under=("api",),
            ),
        )
        result = Shikumi(
            structure=PackageTreeStructure(),
            information_types=[marker_type],
            descriptor_rules=[rule],
        ).validate(package)

        assert result.is_valid
        assert result.diagnostics == ()
    finally:
        for name in tuple(sys.modules):
            if name == "descriptor_path_package" or name.startswith(
                "descriptor_path_package."
            ):
                sys.modules.pop(name, None)
        sys.modules.pop(fixture.__name__, None)
