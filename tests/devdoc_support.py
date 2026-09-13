from __future__ import annotations

from pathlib import Path
import tomllib

from shikumi_devdoc.realizers.changelog_markdown import ChangelogMarkdownRealizer
from shikumi_devdoc.realizers.document_markdown import MarkdownRealizer as DocumentMarkdownRealizer
from shikumi_devdoc.realizers.glossary_markdown import MarkdownRealizer as GlossaryMarkdownRealizer


def project_context() -> dict[str, dict[str, str]]:
    with Path("pyproject.toml").open("rb") as stream:
        project = tomllib.load(stream)["project"]
    scripts = project.get("scripts", {})
    return {
        "PROJECT": {
            "name": project["name"],
            "version": project["version"],
            "requires_python": project["requires-python"],
            "distribution": project["name"],
            "import_package": "shikumi",
            "cli_entry_point": next(iter(scripts), project["name"]),
        }
    }


document_markdown = DocumentMarkdownRealizer(project_context())
changelog_markdown = ChangelogMarkdownRealizer(project_context())
glossary_markdown = GlossaryMarkdownRealizer(project_context())
