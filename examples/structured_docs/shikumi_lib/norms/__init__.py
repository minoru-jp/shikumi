"""Norms for the structured-document example."""

from shikumi import Diagnostic, InformationType, Shikumi, StructuralKind, validator
from shikumi.standard import PackageTreeStructure, assignment, content_type, decorator, docstring, information_type_rule


Command = InformationType("command", str)
Category = InformationType("category", str)
Content = content_type("content")

command = decorator(Command)
category = assignment(Category)
content = docstring(Content, required=True)

@validator(focus=StructuralKind.ENTITY)
def entry_shape(view):
    """Every catalog entry supplies the information required by the norms."""

    for information_type in (Command, Category, Content):
        if len(view.focused.values(information_type)) != 1:
            yield Diagnostic(
                f"catalog entries require exactly one {information_type.name}",
                code="structured_docs.entry.required",
            )


structured_docs = Shikumi(
    structure=PackageTreeStructure(),
    information_types=[Command, Category, Content],
    validators=[
        information_type_rule(Command),
        information_type_rule(Category),
        information_type_rule(Content),
        entry_shape,
    ],
)
