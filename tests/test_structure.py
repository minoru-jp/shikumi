from __future__ import annotations

import types

import pytest

from shikumi import (
    Focus,
    PythonStructure,
    StructuralKind,
    UnsupportedFocusError,
)


def _module(name: str, source: str) -> types.ModuleType:
    module = types.ModuleType(name)
    exec(compile(source, f"<{name}>", "exec"), module.__dict__)
    return module


def test_class_can_be_a_focus_directly() -> None:
    class Entity:
        pass

    resolved = PythonStructure().resolve(Focus(Entity))

    assert len(resolved.nodes) == 1
    assert resolved.nodes[0].subject is Entity
    assert resolved.nodes[0].kind is StructuralKind.ENTITY


def test_module_focus_contains_only_locally_defined_classes() -> None:
    external = _module("example.external", "class Imported: pass")
    module = types.ModuleType("example.page")
    module.Imported = external.Imported
    exec(compile("class Local: pass", "<example.page>", "exec"), module.__dict__)

    resolved = PythonStructure().resolve(Focus(module))

    assert [node.kind for node in resolved.nodes] == [
        StructuralKind.MODULE,
        StructuralKind.ENTITY,
    ]
    assert [node.name for node in resolved.nodes] == ["page", "Local"]
    assert resolved.nodes[1].parent is module


def test_module_focus_contains_lexically_nested_classes() -> None:
    module = _module(
        "example.nested",
        """
class Guide:
    class Section:
        class Note:
            pass
""",
    )

    resolved = PythonStructure().resolve(Focus(module))

    assert [node.path for node in resolved.nodes] == [
        ("example", "nested"),
        ("example", "nested", "Guide"),
        ("example", "nested", "Guide", "Section"),
        ("example", "nested", "Guide", "Section", "Note"),
    ]
    Guide = module.Guide
    assert resolved.nodes[1].parent is module
    assert resolved.nodes[2].parent is Guide
    assert resolved.nodes[3].parent is Guide.Section


def test_class_aliases_are_not_reinterpreted_as_nested_entities() -> None:
    module = _module(
        "example.aliases",
        """
class Shared:
    pass

class Container:
    Alias = Shared
""",
    )

    resolved = PythonStructure().resolve(Focus(module))

    assert [node.name for node in resolved.nodes] == [
        "aliases",
        "Shared",
        "Container",
    ]


def test_package_is_classified_without_importing_children() -> None:
    package = types.ModuleType("example.docs")
    package.__path__ = ["/virtual/example/docs"]

    resolved = PythonStructure().resolve(Focus(package))

    assert len(resolved.nodes) == 1
    assert resolved.nodes[0].kind is StructuralKind.PACKAGE


def test_unsupported_focus_is_rejected_by_structure() -> None:
    with pytest.raises(UnsupportedFocusError):
        PythonStructure().resolve(Focus(object()))


def test_resolved_structure_rejects_duplicate_paths() -> None:
    from shikumi import ResolvedStructure, StructureNode

    root = object()
    child = object()
    focus = Focus(root)

    with pytest.raises(ValueError, match="duplicate path"):
        ResolvedStructure(
            focus=focus,
            nodes=(
                StructureNode(root, StructuralKind.MODULE, "root", ("root",)),
                StructureNode(child, StructuralKind.ENTITY, "Child", ("root",)),
            ),
        )


def test_resolved_structure_rejects_duplicate_subject_identity() -> None:
    from shikumi import ResolvedStructure, StructureNode

    root = object()
    child = object()
    focus = Focus(root)

    with pytest.raises(ValueError, match="duplicate subject identity"):
        ResolvedStructure(
            focus=focus,
            nodes=(
                StructureNode(root, StructuralKind.MODULE, "root", ("root",)),
                StructureNode(child, StructuralKind.ENTITY, "Child", ("root", "Child")),
                StructureNode(
                    child,
                    StructuralKind.ENTITY,
                    "Alias",
                    ("root", "Alias"),
                ),
            ),
        )


def test_resolved_structure_rejects_focus_subject_multiple_times() -> None:
    from shikumi import ResolvedStructure, StructureNode

    root = object()
    focus = Focus(root)

    with pytest.raises(ValueError, match="focus subject exactly once"):
        ResolvedStructure(
            focus=focus,
            nodes=(
                StructureNode(root, StructuralKind.MODULE, "root", ("root",)),
                StructureNode(root, StructuralKind.ENTITY, "again", ("root", "again")),
            ),
        )


def test_resolved_structure_rejects_nodes_outside_focus_root() -> None:
    from shikumi import ResolvedStructure, StructureNode

    root = object()
    child = object()
    focus = Focus(root)

    with pytest.raises(ValueError, match="outside its focus root"):
        ResolvedStructure(
            focus=focus,
            nodes=(
                StructureNode(root, StructuralKind.MODULE, "root", ("root",)),
                StructureNode(child, StructuralKind.ENTITY, "Child", ("other", "Child")),
            ),
        )


def test_resolved_structure_rejects_missing_structural_parent_path() -> None:
    from shikumi import ResolvedStructure, StructureNode

    root = object()
    child = object()
    focus = Focus(root)

    with pytest.raises(ValueError, match="has no parent"):
        ResolvedStructure(
            focus=focus,
            nodes=(
                StructureNode(root, StructuralKind.MODULE, "root", ("root",)),
                StructureNode(
                    child,
                    StructuralKind.ENTITY,
                    "Child",
                    ("root", "missing", "Child"),
                ),
            ),
        )
