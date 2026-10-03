from __future__ import annotations

import types

import pytest

from shikumi import (
    Focus,
    Shikumi,
    StructuralKind,
    StructureElement,
    StructureSpecification,
)


def _module(name: str, source: str) -> types.ModuleType:
    module = types.ModuleType(name)
    exec(compile(source, f"<{name}>", "exec"), module.__dict__)  # noqa: S102 - trusted in-test source is executed intentionally
    return module


def test_structure_specification_can_be_authored_explicitly() -> None:
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("api",), StructuralKind.PACKAGE),
            StructureElement(("api", "users"), StructuralKind.MODULE),
            StructureElement(("api", "users", "GetUser"), StructuralKind.ENTITY),
        ]
    )

    assert specification.element_at(("api", "users")).kind is StructuralKind.MODULE
    assert [element.path for element in specification.subtree(("api", "users"))] == [
        ("api", "users"),
        ("api", "users", "GetUser"),
    ]


def test_structure_specification_requires_a_complete_parent_chain() -> None:
    with pytest.raises(ValueError, match="no parent"):
        StructureSpecification(
            [
                StructureElement((), StructuralKind.PACKAGE),
                StructureElement(("api", "users"), StructuralKind.MODULE),
            ]
        )


def test_structure_specification_can_be_derived_from_a_description_body() -> None:
    reference = _module(
        "reference.users",
        """
class GetUser:
    class Response:
        pass
""",
    )

    specification = Shikumi().derive_structure_specification(reference)

    assert [(element.path, element.kind) for element in specification.elements] == [
        ((), StructuralKind.MODULE),
        (("GetUser",), StructuralKind.ENTITY),
        (("GetUser", "Response"), StructuralKind.ENTITY),
    ]


def test_standalone_module_validation_requires_explicit_placement() -> None:
    module = _module("scratch.users", "class GetUser: pass")

    with pytest.raises(ValueError, match="explicit placement"):
        Shikumi().validate(module)


def test_module_is_checked_against_the_specification_subtree_at_placement() -> None:
    module = _module("scratch.generated", "class GetUser: pass")
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("api",), StructuralKind.PACKAGE),
            StructureElement(("api", "users"), StructuralKind.MODULE),
            StructureElement(("api", "users", "GetUser"), StructuralKind.ENTITY),
            StructureElement(("api", "articles"), StructuralKind.MODULE),
        ]
    )

    result = Shikumi().validate(
        module,
        placement=("api", "users"),
        structure_specification=specification,
    )

    assert result.is_valid
    assert result.structure_check is not None
    assert result.structure_check.is_valid
    assert result.view.focused.node.path == ("api", "users")
    assert result.view.entities[0].node.path == ("api", "users", "GetUser")


def test_structure_check_reports_missing_and_unexpected_elements() -> None:
    module = _module("scratch.generated", "class Other: pass")
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.MODULE),
            StructureElement(("Expected",), StructuralKind.ENTITY),
        ]
    )

    result = Shikumi().validate(
        module,
        placement=(),
        structure_specification=specification,
    )

    assert not result.is_valid
    assert {diagnostic.code for diagnostic in result.diagnostics} == {
        "structure.element.missing",
        "structure.element.unexpected",
    }


def test_structure_check_rejects_an_undefined_placement() -> None:
    module = _module("scratch.generated", "class Item: pass")
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("known",), StructuralKind.MODULE),
        ]
    )

    result = Shikumi().validate(
        Focus(module, placement=("unknown",)),
        structure_specification=specification,
    )

    assert not result.is_valid
    assert result.diagnostics[0].code == "structure.placement.undefined"


def _open_subtree_spec() -> StructureSpecification:
    from shikumi import StructureFragment

    return StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("EXCEPTION",), StructuralKind.PACKAGE),
            StructureElement(("known",), StructuralKind.MODULE),
        ],
        mounts=(
            StructureFragment.unconstrained(StructuralKind.PACKAGE).at(("EXCEPTION",)),
        ),
    )


def test_placement_below_an_unconstrained_subtree_is_accepted() -> None:
    module = _module("scratch.generated", "class Item: pass")

    result = Shikumi().validate(
        Focus(module, placement=("EXCEPTION", "anything", "deep")),
        structure_specification=_open_subtree_spec(),
    )

    assert result.is_valid
    assert not result.diagnostics


def test_undefined_placement_is_rejected_on_the_dynamic_path() -> None:
    module = _module("scratch.generated", "class Item: pass")

    result = Shikumi().validate(
        Focus(module, placement=("unknown",)),
        structure_specification=_open_subtree_spec(),
    )

    assert not result.is_valid
    assert [diagnostic.code for diagnostic in result.diagnostics] == [
        "structure.placement.undefined"
    ]


def _resolved_structure(
    entries: list[tuple[tuple[str, ...], StructuralKind]],
    *,
    placement: tuple[str, ...] | None = None,
):
    from shikumi import ResolvedStructure, StructureNode

    if not entries or entries[0][0] != ():
        raise ValueError("entries must begin with the focus root")

    subjects: dict[tuple[str, ...], object] = {path: object() for path, _ in entries}
    root_subject = subjects[()]
    runtime_root = ("runtime",)
    nodes = []
    for relative, kind in entries:
        path = runtime_root + relative
        parent = subjects.get(relative[:-1]) if relative else None
        name = relative[-1] if relative else "runtime"
        nodes.append(
            StructureNode(
                subject=subjects[relative],
                kind=kind,
                name=name,
                path=path,
                parent=parent,
            )
        )
    return ResolvedStructure(
        focus=Focus(root_subject, placement=placement),
        nodes=tuple(nodes),
    )


def test_structure_fragment_can_be_reused_at_multiple_exact_paths() -> None:
    from shikumi import StructureFragment

    common = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("shared",), StructuralKind.MODULE),
        ]
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("left",), StructuralKind.PACKAGE),
            StructureElement(("right",), StructuralKind.PACKAGE),
        ],
        mounts=(common.at(("left",)), common.at(("right",))),
    )

    assert specification.element_at(("left", "shared")) == StructureElement(
        ("left", "shared"), StructuralKind.MODULE
    )
    assert specification.element_at(("right", "shared")) == StructureElement(
        ("right", "shared"), StructuralKind.MODULE
    )


def test_logical_structure_element_applies_one_rule_to_arbitrary_names() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    actor = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("GUI",), StructuralKind.PACKAGE),
        ]
    )
    logical_actor = LogicalStructureElement(
        parent=("INTERACTION",),
        logical_name="actor",
        fragment=actor,
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
        ],
        logical_elements=(logical_actor,),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("INTERACTION",), StructuralKind.PACKAGE),
            (("INTERACTION", "USER"), StructuralKind.PACKAGE),
            (("INTERACTION", "USER", "GUI"), StructuralKind.PACKAGE),
            (("INTERACTION", "ADMIN"), StructuralKind.PACKAGE),
            (("INTERACTION", "ADMIN", "GUI"), StructuralKind.PACKAGE),
        ]
    )

    result = check_structure(structure, specification)

    assert result.is_valid
    assert [
        (item.logical_element.logical_name, item.actual_path)
        for item in result.bindings
    ] == [
        ("actor", ("INTERACTION", "USER")),
        ("actor", ("INTERACTION", "ADMIN")),
    ]


def test_explicit_structure_element_overrides_logical_name_binding() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    actor = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("GUI",), StructuralKind.PACKAGE),
        ]
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION", "NON_SWDESC"), StructuralKind.PACKAGE),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=("INTERACTION",),
                logical_name="actor",
                fragment=actor,
                min_count=0,
            ),
        ),
        mounts=(
            StructureFragment.unconstrained(StructuralKind.PACKAGE).at(
                ("INTERACTION", "NON_SWDESC")
            ),
        ),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("INTERACTION",), StructuralKind.PACKAGE),
            (("INTERACTION", "NON_SWDESC"), StructuralKind.PACKAGE),
            (("INTERACTION", "NON_SWDESC", "anything"), StructuralKind.PACKAGE),
            (
                ("INTERACTION", "NON_SWDESC", "anything", "module"),
                StructuralKind.MODULE,
            ),
        ]
    )

    result = check_structure(structure, specification)

    assert result.is_valid
    assert result.bindings == ()


def test_logical_structure_element_can_restrict_concrete_names() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    actor = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=("INTERACTION",),
                logical_name="actor",
                fragment=actor,
                names=("USER", "ADMIN"),
                min_count=0,
            ),
        ),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("INTERACTION",), StructuralKind.PACKAGE),
            (("INTERACTION", "CUSTOMER"), StructuralKind.PACKAGE),
        ]
    )

    result = check_structure(structure, specification)

    assert not result.is_valid
    assert [item.code for item in result.diagnostics] == [
        "structure.element.unexpected"
    ]


def test_logical_structure_element_enforces_cardinality() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    actor = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=("INTERACTION",),
                logical_name="actor",
                fragment=actor,
                min_count=1,
                max_count=1,
            ),
        ),
    )

    missing = check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("INTERACTION",), StructuralKind.PACKAGE),
            ]
        ),
        specification,
    )
    too_many = check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("INTERACTION",), StructuralKind.PACKAGE),
                (("INTERACTION", "USER"), StructuralKind.PACKAGE),
                (("INTERACTION", "ADMIN"), StructuralKind.PACKAGE),
            ]
        ),
        specification,
    )

    assert [item.code for item in missing.diagnostics] == ["structure.logical.minimum"]
    assert [item.code for item in too_many.diagnostics] == ["structure.logical.maximum"]


def test_structure_specification_rejects_multiple_logical_elements_at_one_parent() -> (
    None
):
    from shikumi import LogicalStructureElement, StructureFragment

    fragment = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])

    with pytest.raises(ValueError, match="at most one logical element"):
        StructureSpecification(
            [
                StructureElement((), StructuralKind.PACKAGE),
                StructureElement(("ROOT",), StructuralKind.PACKAGE),
            ],
            logical_elements=(
                LogicalStructureElement(
                    parent=("ROOT",),
                    logical_name="actor",
                    fragment=fragment,
                ),
                LogicalStructureElement(
                    parent=("ROOT",),
                    logical_name="service",
                    fragment=fragment,
                ),
            ),
        )


def test_placement_can_traverse_a_logical_structure_element() -> None:
    from shikumi import (
        LogicalStructureElement,
        ResolvedStructure,
        StructureFragment,
        StructureNode,
        check_structure,
    )

    actor = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("GUI",), StructuralKind.MODULE),
        ]
    )
    logical_actor = LogicalStructureElement(
        parent=("INTERACTION",),
        logical_name="actor",
        fragment=actor,
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
        ],
        logical_elements=(logical_actor,),
    )

    module = object()
    structure = ResolvedStructure(
        focus=Focus(module, placement=("INTERACTION", "USER", "GUI")),
        nodes=(
            StructureNode(
                module,
                StructuralKind.MODULE,
                "generated",
                ("runtime", "generated"),
            ),
        ),
    )

    result = check_structure(structure, specification)

    assert result.is_valid
    assert len(result.bindings) == 1
    assert result.bindings[0].logical_element is logical_actor
    assert result.bindings[0].actual_path == ("INTERACTION", "USER")


def test_logical_structure_elements_can_be_nested_for_free_and_enumerated_names() -> (
    None
):
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    medium = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    actor = StructureFragment(
        [StructureElement((), StructuralKind.PACKAGE)],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="medium",
                fragment=medium,
                names=("GUI", "CUI", "PROGRAMMATIC"),
                min_count=1,
                max_count=3,
            ),
        ),
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=("INTERACTION",),
                logical_name="actor",
                fragment=actor,
            ),
        ),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("INTERACTION",), StructuralKind.PACKAGE),
            (("INTERACTION", "USER"), StructuralKind.PACKAGE),
            (("INTERACTION", "USER", "GUI"), StructuralKind.PACKAGE),
            (("INTERACTION", "ADMIN"), StructuralKind.PACKAGE),
            (("INTERACTION", "ADMIN", "CUI"), StructuralKind.PACKAGE),
            (("INTERACTION", "ADMIN", "PROGRAMMATIC"), StructuralKind.PACKAGE),
        ]
    )

    result = check_structure(structure, specification)

    assert result.is_valid
    assert [binding.logical_element.logical_name for binding in result.bindings] == [
        "actor",
        "medium",
        "actor",
        "medium",
        "medium",
    ]
    assert [binding.actual_path[-1] for binding in result.bindings] == [
        "USER",
        "GUI",
        "ADMIN",
        "CUI",
        "PROGRAMMATIC",
    ]


def test_logical_names_must_be_an_iterable_of_complete_names() -> None:
    from shikumi import LogicalStructureElement, StructureFragment

    fragment = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])

    with pytest.raises(TypeError, match="not a string"):
        LogicalStructureElement(
            parent=(),
            logical_name="actor",
            fragment=fragment,
            names="USER",
        )


def test_logical_minimum_must_remain_satisfiable_after_explicit_overrides() -> None:
    from shikumi import LogicalStructureElement, StructureFragment

    fragment = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])

    with pytest.raises(ValueError, match="cannot be satisfied"):
        StructureSpecification(
            [
                StructureElement((), StructuralKind.PACKAGE),
                StructureElement(("USER",), StructuralKind.PACKAGE),
            ],
            logical_elements=(
                LogicalStructureElement(
                    parent=(),
                    logical_name="actor",
                    fragment=fragment,
                    names=("USER",),
                    min_count=1,
                ),
            ),
        )


def test_fragment_mount_rebases_nested_logical_elements() -> None:
    from shikumi import LogicalStructureElement, StructureFragment

    actor = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    interaction = StructureFragment(
        [StructureElement((), StructuralKind.PACKAGE)],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="actor",
                fragment=actor,
                min_count=0,
            ),
        ),
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("PRIMARY",), StructuralKind.PACKAGE),
            StructureElement(("SECONDARY",), StructuralKind.PACKAGE),
        ],
        mounts=(interaction.at(("PRIMARY",)), interaction.at(("SECONDARY",))),
    )

    assert [element.parent for element in specification.logical_elements] == [
        ("PRIMARY",),
        ("SECONDARY",),
    ]


def test_logical_structure_element_checks_bound_instance_kind() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    actor = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=("INTERACTION",),
                logical_name="actor",
                fragment=actor,
            ),
        ),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("INTERACTION",), StructuralKind.PACKAGE),
            (("INTERACTION", "USER"), StructuralKind.MODULE),
        ]
    )

    result = check_structure(structure, specification)

    assert [item.code for item in result.diagnostics] == ["structure.kind.mismatch"]
    assert [
        (item.logical_element.logical_name, item.actual_path)
        for item in result.bindings
    ] == [
        ("actor", ("INTERACTION", "USER")),
    ]


def test_unconstrained_fragment_is_distinct_from_a_closed_leaf() -> None:
    from shikumi import StructureFragment, check_structure

    elements = [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("EXCEPTION",), StructuralKind.PACKAGE),
    ]
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("EXCEPTION",), StructuralKind.PACKAGE),
            (("EXCEPTION", "anything"), StructuralKind.MODULE),
        ]
    )

    closed = check_structure(structure, StructureSpecification(elements))
    open_subtree = check_structure(
        structure,
        StructureSpecification(
            elements,
            mounts=(
                StructureFragment.unconstrained(StructuralKind.PACKAGE).at(
                    ("EXCEPTION",)
                ),
            ),
        ),
    )

    assert [item.code for item in closed.diagnostics] == [
        "structure.element.unexpected"
    ]
    assert open_subtree.is_valid


def test_explicit_exception_does_not_count_toward_logical_cardinality() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    actor = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION", "USER"), StructuralKind.PACKAGE),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=("INTERACTION",),
                logical_name="actor",
                fragment=actor,
                names=("USER", "ADMIN"),
                min_count=1,
            ),
        ),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("INTERACTION",), StructuralKind.PACKAGE),
            (("INTERACTION", "USER"), StructuralKind.PACKAGE),
        ]
    )

    result = check_structure(structure, specification)

    assert [item.code for item in result.diagnostics] == ["structure.logical.minimum"]
    assert result.bindings == ()


def test_optional_exact_element_may_be_absent_without_activating_descendants() -> None:
    from shikumi import check_structure

    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("API",), StructuralKind.PACKAGE, required=False),
            StructureElement(("API", "TYPES"), StructuralKind.PACKAGE),
            StructureElement(("API", "CONTRACTS"), StructuralKind.PACKAGE),
        ]
    )
    structure = _resolved_structure([((), StructuralKind.PACKAGE)])

    result = check_structure(structure, specification)

    assert result.is_valid
    assert result.diagnostics == ()


def test_optional_exact_element_activates_required_descendants_when_present() -> None:
    from shikumi import check_structure

    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("API",), StructuralKind.PACKAGE, required=False),
            StructureElement(("API", "TYPES"), StructuralKind.PACKAGE),
            StructureElement(("API", "CONTRACTS"), StructuralKind.PACKAGE),
        ]
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("API",), StructuralKind.PACKAGE),
            (("API", "TYPES"), StructuralKind.PACKAGE),
        ]
    )

    result = check_structure(structure, specification)

    assert [item.code for item in result.diagnostics] == ["structure.element.missing"]
    assert "API.CONTRACTS" in result.diagnostics[0].message


def test_optional_exact_element_still_precedes_logical_binding_when_present() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    actor = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE),
            StructureElement(
                ("INTERACTION", "MATERIALS"),
                StructuralKind.PACKAGE,
                required=False,
            ),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=("INTERACTION",),
                logical_name="actor",
                fragment=actor,
                min_count=0,
            ),
        ),
        mounts=(
            StructureFragment.unconstrained(StructuralKind.PACKAGE).at(
                ("INTERACTION", "MATERIALS")
            ),
        ),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("INTERACTION",), StructuralKind.PACKAGE),
            (("INTERACTION", "USER"), StructuralKind.PACKAGE),
            (("INTERACTION", "MATERIALS"), StructuralKind.PACKAGE),
            (("INTERACTION", "MATERIALS", "free"), StructuralKind.MODULE),
        ]
    )

    result = check_structure(structure, specification)

    assert result.is_valid
    assert [binding.actual_path for binding in result.bindings] == [
        ("INTERACTION", "USER")
    ]


def test_optional_mount_target_activates_fragment_only_when_present() -> None:
    from shikumi import StructureFragment, check_structure

    api = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("TYPES",), StructuralKind.PACKAGE),
        ]
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("API",), StructuralKind.PACKAGE, required=False),
        ],
        mounts=(api.at(("API",)),),
    )

    absent = check_structure(
        _resolved_structure([((), StructuralKind.PACKAGE)]),
        specification,
    )
    present_but_incomplete = check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("API",), StructuralKind.PACKAGE),
            ]
        ),
        specification,
    )

    assert absent.is_valid
    assert [item.code for item in present_but_incomplete.diagnostics] == [
        "structure.element.missing"
    ]
    assert "API.TYPES" in present_but_incomplete.diagnostics[0].message


def test_fragment_mount_preserves_optional_child_semantics() -> None:
    from shikumi import StructureFragment, check_structure

    fragment = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("MATERIALS",), StructuralKind.PACKAGE, required=False),
        ]
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("AREA",), StructuralKind.PACKAGE),
        ],
        mounts=(fragment.at(("AREA",)),),
    )

    assert specification.element_at(("AREA", "MATERIALS")) == StructureElement(
        ("AREA", "MATERIALS"),
        StructuralKind.PACKAGE,
        required=False,
    )
    assert check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("AREA",), StructuralKind.PACKAGE),
            ]
        ),
        specification,
    ).is_valid


def test_structure_regulation_root_cannot_be_optional() -> None:
    from shikumi import StructureFragment

    with pytest.raises(ValueError, match="root element must be required"):
        StructureSpecification(
            [StructureElement((), StructuralKind.PACKAGE, required=False)]
        )

    with pytest.raises(ValueError, match="root element must be required"):
        StructureFragment(
            [StructureElement((), StructuralKind.PACKAGE, required=False)]
        )


def test_structure_element_required_must_be_bool() -> None:
    with pytest.raises(TypeError, match="required must be a bool"):
        StructureElement((), StructuralKind.PACKAGE, required=1)  # type: ignore[arg-type]


def test_optional_parent_does_not_activate_logical_cardinality_until_present() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    medium = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    interaction = StructureFragment(
        [StructureElement((), StructuralKind.PACKAGE)],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="actor",
                fragment=medium,
                min_count=1,
            ),
        ),
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(
                ("INTERACTION",),
                StructuralKind.PACKAGE,
                required=False,
            ),
        ],
        mounts=(interaction.at(("INTERACTION",)),),
    )

    absent = check_structure(
        _resolved_structure([((), StructuralKind.PACKAGE)]),
        specification,
    )
    present_without_actor = check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("INTERACTION",), StructuralKind.PACKAGE),
            ]
        ),
        specification,
    )

    assert absent.is_valid
    assert [item.code for item in present_without_actor.diagnostics] == [
        "structure.logical.minimum"
    ]


def test_optional_sections_compose_a_software_description_style_regulation() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    open_package = StructureFragment.unconstrained(StructuralKind.PACKAGE)
    medium = StructureFragment.unconstrained(StructuralKind.PACKAGE)
    actor = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(
                ("MATERIALS",),
                StructuralKind.PACKAGE,
                required=False,
            ),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="medium",
                fragment=medium,
                names=("GUI", "CUI", "PROGRAMMATIC"),
                min_count=1,
                max_count=3,
            ),
        ),
        mounts=(open_package.at(("MATERIALS",)),),
    )
    interaction = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(
                ("MATERIALS",),
                StructuralKind.PACKAGE,
                required=False,
            ),
            StructureElement(
                ("NON_SWDESC",),
                StructuralKind.PACKAGE,
                required=False,
            ),
        ],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="actor",
                fragment=actor,
                min_count=1,
            ),
        ),
        mounts=(
            open_package.at(("MATERIALS",)),
            open_package.at(("NON_SWDESC",)),
        ),
    )
    api_section = StructureFragment.unconstrained(StructuralKind.PACKAGE)
    api = StructureFragment(
        [StructureElement((), StructuralKind.PACKAGE)],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="api_section",
                fragment=api_section,
                names=("TYPES", "CONTRACTS", "PROCESS"),
                min_count=1,
                max_count=3,
            ),
        ),
    )

    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("CONCEPTS",), StructuralKind.PACKAGE, required=False),
            StructureElement(("INTERACTION",), StructuralKind.PACKAGE, required=False),
            StructureElement(("API",), StructuralKind.PACKAGE, required=False),
        ],
        mounts=(
            open_package.at(("CONCEPTS",)),
            interaction.at(("INTERACTION",)),
            api.at(("API",)),
        ),
    )

    concepts_only = check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("CONCEPTS",), StructuralKind.PACKAGE),
                (("CONCEPTS", "domain"), StructuralKind.MODULE),
            ]
        ),
        specification,
    )
    full = check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("INTERACTION",), StructuralKind.PACKAGE),
                (("INTERACTION", "USER"), StructuralKind.PACKAGE),
                (("INTERACTION", "USER", "GUI"), StructuralKind.PACKAGE),
                (("INTERACTION", "MATERIALS"), StructuralKind.PACKAGE),
                (("INTERACTION", "MATERIALS", "diagram"), StructuralKind.MODULE),
                (("API",), StructuralKind.PACKAGE),
                (("API", "TYPES"), StructuralKind.PACKAGE),
            ]
        ),
        specification,
    )

    assert concepts_only.is_valid
    assert full.is_valid
    assert [binding.logical_element.logical_name for binding in full.bindings] == [
        "actor",
        "medium",
        "api_section",
    ]


def test_logical_structure_elements_can_share_a_parent_when_kinds_differ() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    package_rule = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])
    module_rule = StructureFragment([StructureElement((), StructuralKind.MODULE)])
    specification = StructureSpecification(
        [StructureElement((), StructuralKind.PACKAGE)],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="package",
                fragment=package_rule,
                min_count=0,
            ),
            LogicalStructureElement(
                parent=(),
                logical_name="module",
                fragment=module_rule,
                min_count=0,
            ),
        ),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("users",), StructuralKind.PACKAGE),
            (("billing",), StructuralKind.PACKAGE),
            (("config",), StructuralKind.MODULE),
        ]
    )

    result = check_structure(structure, specification)

    assert result.is_valid
    assert [
        (item.logical_element.logical_name, item.actual_path)
        for item in result.bindings
    ] == [
        ("package", ("users",)),
        ("package", ("billing",)),
        ("module", ("config",)),
    ]


def test_structure_specification_rejects_two_logical_elements_of_the_same_kind_at_one_parent() -> (
    None
):
    from shikumi import LogicalStructureElement, StructureFragment

    package_rule = StructureFragment([StructureElement((), StructuralKind.PACKAGE)])

    with pytest.raises(
        ValueError, match="at most one logical element per structural kind"
    ):
        StructureSpecification(
            [StructureElement((), StructuralKind.PACKAGE)],
            logical_elements=(
                LogicalStructureElement(
                    parent=(),
                    logical_name="actor",
                    fragment=package_rule,
                    min_count=0,
                ),
                LogicalStructureElement(
                    parent=(),
                    logical_name="service",
                    fragment=package_rule,
                    min_count=0,
                ),
            ),
        )


def test_recursive_structure_fragment_reapplies_itself_to_any_observed_depth() -> None:
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    module_rule = StructureFragment([StructureElement((), StructuralKind.MODULE)])
    package_tree = StructureFragment(
        [StructureElement((), StructuralKind.PACKAGE)],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="module",
                fragment=module_rule,
                min_count=0,
            ),
        ),
    ).recursive(logical_name="package")
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("src",), StructuralKind.PACKAGE),
        ],
        mounts=(package_tree.at(("src",)),),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("src",), StructuralKind.PACKAGE),
            (("src", "users"), StructuralKind.PACKAGE),
            (("src", "users", "models"), StructuralKind.PACKAGE),
            (("src", "users", "models", "account"), StructuralKind.MODULE),
            (("src", "config"), StructuralKind.MODULE),
        ]
    )

    result = check_structure(structure, specification)

    assert result.is_valid
    assert [
        (item.logical_element.logical_name, item.actual_path)
        for item in result.bindings
    ] == [
        ("package", ("src", "users")),
        ("package", ("src", "users", "models")),
        ("module", ("src", "users", "models", "account")),
        ("module", ("src", "config")),
    ]


def test_recursive_structure_fragment_can_limit_sibling_count() -> None:
    from shikumi import StructureFragment, check_structure

    package_tree = StructureFragment(
        [StructureElement((), StructuralKind.PACKAGE)]
    ).recursive(logical_name="package", max_count=1)
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("src",), StructuralKind.PACKAGE),
        ],
        mounts=(package_tree.at(("src",)),),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("src",), StructuralKind.PACKAGE),
            (("src", "a"), StructuralKind.PACKAGE),
            (("src", "b"), StructuralKind.PACKAGE),
        ]
    )

    result = check_structure(structure, specification)

    assert [item.code for item in result.diagnostics] == ["structure.logical.maximum"]


def test_structure_group_constrains_presence_across_different_exact_rules() -> None:
    from shikumi import StructureGroup, check_structure

    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("LOCAL",), StructuralKind.PACKAGE, required=False),
            StructureElement(("REMOTE",), StructuralKind.PACKAGE, required=False),
        ],
        groups=(
            StructureGroup(
                parent=(),
                members=("LOCAL", "REMOTE"),
                min_count=1,
                max_count=1,
            ),
        ),
    )

    local_only = check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("LOCAL",), StructuralKind.PACKAGE),
            ]
        ),
        specification,
    )
    neither = check_structure(
        _resolved_structure([((), StructuralKind.PACKAGE)]),
        specification,
    )
    both = check_structure(
        _resolved_structure(
            [
                ((), StructuralKind.PACKAGE),
                (("LOCAL",), StructuralKind.PACKAGE),
                (("REMOTE",), StructuralKind.PACKAGE),
            ]
        ),
        specification,
    )

    assert local_only.is_valid
    assert [item.code for item in neither.diagnostics] == ["structure.group.minimum"]
    assert [item.code for item in both.diagnostics] == ["structure.group.maximum"]


def test_structure_group_is_reused_when_its_fragment_is_mounted() -> None:
    from shikumi import StructureFragment, StructureGroup, check_structure

    auth = StructureFragment(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("LOCAL",), StructuralKind.PACKAGE, required=False),
            StructureElement(("REMOTE",), StructuralKind.PACKAGE, required=False),
        ],
        groups=(
            StructureGroup(
                parent=(),
                members=("LOCAL", "REMOTE"),
                min_count=1,
                max_count=1,
            ),
        ),
    )
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("AUTH",), StructuralKind.PACKAGE),
        ],
        mounts=(auth.at(("AUTH",)),),
    )
    structure = _resolved_structure(
        [
            ((), StructuralKind.PACKAGE),
            (("AUTH",), StructuralKind.PACKAGE),
        ]
    )

    result = check_structure(structure, specification)

    assert [item.code for item in result.diagnostics] == ["structure.group.minimum"]


def test_placement_can_disambiguate_kind_specific_logical_rules_from_remaining_structure() -> (
    None
):
    from shikumi import LogicalStructureElement, StructureFragment, check_structure

    module_rule = StructureFragment([StructureElement((), StructuralKind.MODULE)])
    package_tree = StructureFragment(
        [StructureElement((), StructuralKind.PACKAGE)],
        logical_elements=(
            LogicalStructureElement(
                parent=(),
                logical_name="module",
                fragment=module_rule,
                min_count=0,
            ),
        ),
    ).recursive(logical_name="package")
    specification = StructureSpecification(
        [
            StructureElement((), StructuralKind.PACKAGE),
            StructureElement(("src",), StructuralKind.PACKAGE),
        ],
        mounts=(package_tree.at(("src",)),),
    )
    standalone_module = _resolved_structure(
        [((), StructuralKind.MODULE)],
        placement=("src", "users", "models"),
    )

    result = check_structure(standalone_module, specification)

    assert result.is_valid
    assert [
        (item.logical_element.logical_name, item.actual_path)
        for item in result.bindings
    ] == [
        ("package", ("src", "users")),
        ("module", ("src", "users", "models")),
    ]
