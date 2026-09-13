"""Markdown realizer for the structured-document example."""

from shikumi import Diagnostic, RealizationCheck, Realizer, SemanticView

from ..norms import Category, Command, Content


class MarkdownRealizer(Realizer[str]):
    def check(self, view: SemanticView) -> RealizationCheck:
        diagnostics: list[Diagnostic] = []
        for item in view.entities:
            if len(item.values(Command)) != 1:
                diagnostics.append(Diagnostic("command name is required", subject=item.subject))
            if len(item.values(Category)) != 1:
                diagnostics.append(Diagnostic("category is required", subject=item.subject))
            if len(item.values(Content)) != 1:
                diagnostics.append(Diagnostic("content is required", subject=item.subject))
        return RealizationCheck(view, tuple(diagnostics))

    def realize(self, view: SemanticView) -> str:
        lines = ["# Command catalog", ""]
        for item in view.entities:
            command = item.values(Command)[0]
            category = item.values(Category)[0]
            content = item.values(Content)[0]
            lines.extend([
                f"## `{command}`",
                "",
                str(content),
                "",
                f"Category: `{category}`",
                "",
            ])
        return "\n".join(lines).rstrip() + "\n"


markdown = MarkdownRealizer()
