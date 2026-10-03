"""Standard structures for package trees backed by Python import paths."""

from __future__ import annotations

from importlib import import_module
from pkgutil import walk_packages
from types import ModuleType

from ..errors import UnsupportedFocusError
from ..structure import (
    Focus,
    PythonStructure,
    ResolvedStructure,
    StructuralKind,
    Structure,
    StructureNode,
)


class PackageTreeStructure(Structure):
    """Interpret an imported package together with its physical module tree.

    Package children are discovered from ``package.__path__`` and imported with
    Python's normal import machinery. Runtime execution therefore remains the
    source of truth for entities and attached information.

    Module and entity foci fall back to :class:`PythonStructure`; recursive
    discovery happens only when the explicit focus is a package. An explicit
    focus placement rebases the resolved tree without changing Python runtime
    identity.
    """

    __slots__: tuple[str, ...] = ("_python",)
    _python: PythonStructure

    def __init__(self) -> None:
        self._python = PythonStructure()

    def resolve(self, focus: Focus) -> ResolvedStructure:
        subject = focus.subject
        if isinstance(subject, ModuleType) and hasattr(subject, "__path__"):
            return self._resolve_package_tree(focus, subject)
        if isinstance(subject, (ModuleType, type)):
            return self._python.resolve(focus)
        raise UnsupportedFocusError(
            f"PackageTreeStructure cannot interpret focus of type "
            f"{type(subject).__name__}"
        )

    def _resolve_package_tree(
        self,
        focus: Focus,
        package: ModuleType,
    ) -> ResolvedStructure:
        modules = self._discover_modules(package)
        by_name = {module.__name__: module for module in modules}
        nodes: list[StructureNode] = []
        source_root = tuple(package.__name__.split("."))
        target_root = focus.placement if focus.placement is not None else source_root

        for module in modules:
            source_path = tuple(module.__name__.split("."))
            relative = source_path[len(source_root) :]
            module_path = target_root + relative
            kind = (
                StructuralKind.PACKAGE
                if hasattr(module, "__path__")
                else StructuralKind.MODULE
            )
            parent = self._module_parent(module, by_name)
            nodes.append(
                StructureNode(
                    subject=module,
                    kind=kind,
                    name=module.__name__.rsplit(".", 1)[-1],
                    path=module_path,
                    parent=parent,
                )
            )

            local = self._python.resolve(Focus(module, placement=module_path))
            nodes.extend(local.nodes[1:])

        return ResolvedStructure(focus=focus, nodes=tuple(nodes))

    @staticmethod
    def _discover_modules(package: ModuleType) -> tuple[ModuleType, ...]:
        discovered: list[ModuleType] = [package]
        prefix = package.__name__ + "."
        infos = sorted(
            walk_packages(package.__path__, prefix=prefix),
            key=lambda info: info.name,
        )
        for info in infos:
            discovered.append(import_module(info.name))
        return tuple(discovered)

    @staticmethod
    def _module_parent(
        module: ModuleType,
        by_name: dict[str, ModuleType],
    ) -> ModuleType | None:
        parent_name, separator, _ = module.__name__.rpartition(".")
        if not separator:
            return None
        return by_name.get(parent_name)
