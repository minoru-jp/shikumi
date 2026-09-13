"""Markdown realization for the Web API example."""

from __future__ import annotations

from shikumi import Diagnostic, RealizationCheck, Realizer, SemanticView

from ..norms import Content, Method, Path, Related, Tag


class MarkdownRealizer(Realizer[str]):
    """Render an API package semantic view as a small Markdown reference."""

    def check(self, view: SemanticView) -> RealizationCheck:
        diagnostics: list[Diagnostic] = []
        for endpoint in view.entities:
            if len(endpoint.values(Method)) != 1:
                diagnostics.append(
                    Diagnostic(
                        "Markdown realization requires exactly one method",
                        code="markdown.method.required",
                        subject=endpoint.subject,
                    )
                )
            if len(endpoint.values(Path)) != 1:
                diagnostics.append(
                    Diagnostic(
                        "Markdown realization requires exactly one path",
                        code="markdown.path.required",
                        subject=endpoint.subject,
                    )
                )
            if len(endpoint.values(Content)) != 1:
                diagnostics.append(
                    Diagnostic(
                        "Markdown realization requires exactly one content value",
                        code="markdown.content.required",
                        subject=endpoint.subject,
                    )
                )
            if any(not isinstance(value, type) for value in endpoint.values(Related)):
                diagnostics.append(
                    Diagnostic(
                        "Markdown realization requires related values to be classes",
                        code="markdown.related.type",
                        subject=endpoint.subject,
                    )
                )
        return RealizationCheck(view, tuple(diagnostics))

    def realize(self, view: SemanticView) -> str:
        lines = ["# Example Web API", ""]

        for module in view.modules:
            endpoints = [
                item
                for item in view.entities
                if item.node.parent is module.subject
            ]
            if not endpoints:
                continue

            lines.extend([f"## `{module.node.name}`", ""])
            for endpoint in endpoints:
                method = endpoint.values(Method)[0]
                path = endpoint.values(Path)[0]
                content = endpoint.values(Content)[0]
                tags = endpoint.values(Tag)
                related = endpoint.values(Related)

                lines.extend(
                    [
                        f"### {method} `{path}`",
                        "",
                        str(content),
                        "",
                    ]
                )
                if tags:
                    lines.extend([f"Tags: {', '.join(map(str, tags))}", ""])
                if related:
                    names = ", ".join(subject.__name__ for subject in related)
                    lines.extend([f"Related: {names}", ""])

        return "\n".join(lines).rstrip() + "\n"


markdown = MarkdownRealizer()
