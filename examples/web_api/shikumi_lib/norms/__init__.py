"""Shikumi composition for the Web API example."""

from __future__ import annotations

from collections import defaultdict

from shikumi import (
    Cardinality,
    DescriptorUseRule,
    Diagnostic,
    InformationType,
    Shikumi,
    StructuralKind,
    StructureElement,
    StructureSelector,
    StructureSpecification,
    validator,
)
from shikumi.standard import (
    PackageTreeStructure,
    assignment,
    content_type,
    docstring,
    information_type_rule,
)


# Semantic information types.  They say what information means, not how it is
# written in Python source.
Method = InformationType("method", str)
Path = InformationType("path", str)
Tag = InformationType("tag", str, cardinality=Cardinality.MANY)
Content = content_type("content")
Related = InformationType("related", type, cardinality=Cardinality.MANY)


# Explicit structural regulation for the description package.  The root package
# name is intentionally absent: paths are relative to the validation focus.
web_api_structure = StructureSpecification(
    [
        StructureElement((), StructuralKind.PACKAGE),
        StructureElement(("articles",), StructuralKind.MODULE),
        StructureElement(("articles", "ListArticles"), StructuralKind.ENTITY),
        StructureElement(("articles", "GetArticle"), StructuralKind.ENTITY),
        StructureElement(("articles", "CreateArticle"), StructuralKind.ENTITY),
        StructureElement(("users",), StructuralKind.MODULE),
        StructureElement(("users", "GetUser"), StructuralKind.ENTITY),
        StructureElement(("users", "ListUsers"), StructuralKind.ENTITY),
        StructureElement(("users", "UpdateUser"), StructuralKind.ENTITY),
    ]
)


# Description writers.  These are merely Python-side ways of writing the
# information types above.
method = assignment(Method)
path = assignment(Path)
tag = assignment(Tag)
related = assignment(Related)
content = docstring(Content)


# Description-writer use is regulated independently from the information each
# writer attaches. All writers in this API specification are intended for
# endpoint entities; unknown writers would remain unrestricted by default.
endpoint_writer_rules = [
    DescriptorUseRule(
        descriptor=writer,
        allowed=StructureSelector(kind=StructuralKind.ENTITY),
        name=name,
    )
    for name, writer in [
        ("method", method),
        ("path", path),
        ("tag", tag),
        ("related", related),
        ("content", content),
    ]
]


_ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


def _single_value(item, information_type: InformationType) -> object | None:
    values = item.values(information_type)
    return values[0] if len(values) == 1 else None


def _route_key(item) -> tuple[str, str] | None:
    method_value = _single_value(item, Method)
    path_value = _single_value(item, Path)
    if not isinstance(method_value, str) or not isinstance(path_value, str):
        return None
    return method_value, path_value


@validator(focus=StructuralKind.ENTITY)
def endpoint_shape(view):
    """Every endpoint needs one method, one path, and non-empty content."""

    endpoint = view.focused

    if not endpoint.has(Method):
        yield Diagnostic("endpoint method is required", code="endpoint.method.required")
    if not endpoint.has(Path):
        yield Diagnostic("endpoint path is required", code="endpoint.path.required")
    if not endpoint.has(Content):
        yield Diagnostic("endpoint description is required", code="endpoint.content.required")

    method_value = _single_value(endpoint, Method)
    if isinstance(method_value, str) and method_value not in _ALLOWED_METHODS:
        yield Diagnostic(
            f"unsupported HTTP method: {method_value}",
            code="endpoint.method.unsupported",
        )

    path_value = _single_value(endpoint, Path)
    if isinstance(path_value, str) and not path_value.startswith("/"):
        yield Diagnostic(
            "endpoint path must start with '/'",
            code="endpoint.path.absolute",
        )


@validator(focus=StructuralKind.MODULE)
def unique_routes_in_module(view):
    """A module must not contain two endpoints with the same route."""

    seen: dict[tuple[str, str], object] = {}
    for endpoint in view.entities:
        route = _route_key(endpoint)
        if route is None:
            continue
        previous = seen.get(route)
        if previous is not None:
            yield Diagnostic(
                f"duplicate route in module: {route[0]} {route[1]}",
                code="endpoint.route.duplicate.module",
                subject=endpoint.subject,
            )
        else:
            seen[route] = endpoint.subject


@validator(focus=StructuralKind.PACKAGE)
def unique_routes_in_package(view):
    """The whole API package must have globally unique method/path pairs."""

    grouped: dict[tuple[str, str], list[object]] = defaultdict(list)
    for endpoint in view.entities:
        route = _route_key(endpoint)
        if route is not None:
            grouped[route].append(endpoint.subject)

    for route, subjects in grouped.items():
        for duplicate in subjects[1:]:
            yield Diagnostic(
                f"duplicate route in API: {route[0]} {route[1]}",
                code="endpoint.route.duplicate.package",
                subject=duplicate,
            )


web_api = Shikumi(
    structure=PackageTreeStructure(),
    information_types=[Method, Path, Tag, Content, Related],
    descriptor_rules=endpoint_writer_rules,
    validators=[
        information_type_rule(Method),
        information_type_rule(Path),
        information_type_rule(Tag),
        information_type_rule(Content),
        information_type_rule(Related),
        endpoint_shape,
        unique_routes_in_module,
        unique_routes_in_package,
    ],
)
