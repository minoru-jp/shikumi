"""Project-local Shikumi norms for the architecture example."""

from __future__ import annotations

from shikumi import Cardinality, Diagnostic, InformationType, Shikumi, StructuralKind, validator
from shikumi.standard import PackageTreeStructure, assignment, decorator, information_type_rule


Layer = InformationType("layer", str)
DependsOn = InformationType("depends on", type, cardinality=Cardinality.MANY)

layer = decorator(Layer)
depends_on = assignment(DependsOn)

_ALLOWED_DEPENDENCIES = {
    "domain": {"domain"},
    "application": {"application", "domain"},
    "infrastructure": {"infrastructure", "domain"},
}


@validator(focus=StructuralKind.ENTITY)
def component_shape(view):
    """Every architecture entity declares exactly one layer."""

    if len(view.focused.values(Layer)) != 1:
        yield Diagnostic(
            "architecture entities require exactly one layer",
            code="architecture.layer.required",
        )


@validator(focus=StructuralKind.PACKAGE)
def dependency_direction(view):
    """Check dependency directions between described architecture entities."""

    by_subject = {item.subject: item for item in view.entities}

    for source in view.entities:
        source_layers = source.values(Layer)
        if len(source_layers) != 1:
            continue
        source_layer = source_layers[0]
        allowed = _ALLOWED_DEPENDENCIES.get(source_layer, set())

        for target_subject in source.values(DependsOn):
            target = by_subject.get(target_subject)
            if target is None:
                yield Diagnostic(
                    "dependency target is outside the interpreted architecture",
                    code="architecture.dependency.external",
                    subject=source.subject,
                )
                continue

            target_layers = target.values(Layer)
            if len(target_layers) != 1:
                continue
            target_layer = target_layers[0]
            if target_layer not in allowed:
                yield Diagnostic(
                    f"{source_layer} must not depend on {target_layer}",
                    code="architecture.dependency.direction",
                    subject=source.subject,
                )


architecture = Shikumi(
    structure=PackageTreeStructure(),
    information_types=[Layer, DependsOn],
    validators=[
        information_type_rule(Layer),
        information_type_rule(DependsOn),
        component_shape,
        dependency_direction,
    ],
)
