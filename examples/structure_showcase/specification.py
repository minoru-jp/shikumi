"""Domain-light structural showcase for Shikumi's structure specification API."""

from __future__ import annotations

from shikumi import (
    LogicalStructureElement,
    Shikumi,
    StructuralKind,
    StructureElement,
    StructureFragment,
    StructureGroup,
    StructureSpecification,
)
from shikumi.standard import PackageTreeStructure


open_package = StructureFragment.unconstrained(StructuralKind.PACKAGE)
closed_package = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
closed_module = StructureFragment([StructureElement((), StructuralKind.MODULE)])

collection = StructureFragment(
    [StructureElement((), StructuralKind.PACKAGE)],
    logical_elements=(
        LogicalStructureElement(
            parent=(),
            logical_name="entry",
            fragment=open_package,
            min_count=1,
        ),
    ),
)

named_collection = StructureFragment(
    [StructureElement((), StructuralKind.PACKAGE)],
    logical_elements=(
        LogicalStructureElement(
            parent=(),
            logical_name="variant",
            fragment=closed_package,
            names=("alpha", "beta", "gamma"),
            min_count=1,
            max_count=2,
        ),
    ),
)

mixed_children = StructureFragment(
    [StructureElement((), StructuralKind.PACKAGE)],
    logical_elements=(
        LogicalStructureElement(
            parent=(),
            logical_name="package_child",
            fragment=closed_package,
            min_count=0,
        ),
        LogicalStructureElement(
            parent=(),
            logical_name="module_child",
            fragment=closed_module,
            min_count=0,
        ),
    ),
)

recursive_tree = StructureFragment(
    [StructureElement((), StructuralKind.PACKAGE)],
    logical_elements=(
        LogicalStructureElement(
            parent=(),
            logical_name="module_leaf",
            fragment=closed_module,
            min_count=0,
        ),
    ),
).recursive(logical_name="branch")

mode_choice = StructureFragment(
    [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("local",), StructuralKind.PACKAGE, required=False),
        StructureElement(("remote",), StructuralKind.PACKAGE, required=False),
    ],
    groups=(
        StructureGroup(
            parent=(),
            members=("local", "remote"),
            min_count=1,
            max_count=1,
        ),
    ),
)

override = StructureFragment(
    [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("special",), StructuralKind.PACKAGE, required=False),
    ],
    logical_elements=(
        LogicalStructureElement(
            parent=(),
            logical_name="ordinary",
            fragment=closed_package,
            min_count=0,
        ),
    ),
    mounts=(open_package.at(("special",)),),
)

showcase_structure = StructureSpecification(
    [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("required",), StructuralKind.PACKAGE),
        StructureElement(("optional",), StructuralKind.PACKAGE, required=False),
        StructureElement(("collection",), StructuralKind.PACKAGE, required=False),
        StructureElement(("named",), StructuralKind.PACKAGE, required=False),
        StructureElement(("mixed",), StructuralKind.PACKAGE, required=False),
        StructureElement(("tree",), StructuralKind.PACKAGE, required=False),
        StructureElement(("mode",), StructuralKind.PACKAGE, required=False),
        StructureElement(("override",), StructuralKind.PACKAGE, required=False),
        StructureElement(("open",), StructuralKind.PACKAGE, required=False),
    ],
    mounts=(
        open_package.at(("optional",)),
        collection.at(("collection",)),
        named_collection.at(("named",)),
        mixed_children.at(("mixed",)),
        recursive_tree.at(("tree",)),
        mode_choice.at(("mode",)),
        override.at(("override",)),
        open_package.at(("open",)),
    ),
)

showcase = Shikumi(structure=PackageTreeStructure())
