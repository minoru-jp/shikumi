from __future__ import annotations

from architecture import body as architecture_body
from architecture.shikumi_lib.norms import architecture
from structured_docs import body as docs_body
from structured_docs.shikumi_lib.norms import structured_docs
from structured_docs.shikumi_lib.realizers.markdown import markdown as docs_markdown
from structure_from_body import candidate, reference
from structure_from_body.reference import catalog as reference_catalog
from structure_from_body.candidate import catalog as candidate_catalog
from structure_from_body.shikumi_lib.norms import structure_only
from web_api import api
from web_api.shikumi_lib.norms import web_api, web_api_structure
from web_api.shikumi_lib.realizers.markdown import markdown as api_markdown


def test_architecture_example_validates_dependency_direction() -> None:
    result = architecture.validate(architecture_body)
    assert result.is_valid, result.diagnostics


def test_structured_docs_example_realizes_markdown() -> None:
    result = structured_docs.validate(docs_body)
    assert result.is_valid, result.diagnostics
    assert docs_markdown.check(result.view).is_realizable
    artifact = docs_markdown.realize(result.view)
    assert "# Command catalog" in artifact
    assert "## `deploy`" in artifact
    assert "## `status`" in artifact


def test_web_api_example_validates_and_realizes() -> None:
    result = web_api.validate(api, structure_specification=web_api_structure)
    assert result.is_valid, result.diagnostics
    assert api_markdown.check(result.view).is_realizable
    assert "### GET `/users/{user_id}`" in api_markdown.realize(result.view)


def test_structure_from_body_checks_structure_not_content() -> None:
    specification = structure_only.derive_structure_specification(reference)
    result = structure_only.validate(candidate, structure_specification=specification)

    assert result.is_valid, result.diagnostics
    assert reference_catalog.ITEM_1.__doc__ != candidate_catalog.ITEM_1.__doc__
