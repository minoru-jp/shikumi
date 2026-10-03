from __future__ import annotations

import os
import re
import subprocess
from inspect import cleandoc
from pathlib import Path

from shikumi_devdoc.norms._document import DocumentField, FieldPresentation, FieldValue
from shikumi_devdoc.norms.document import system as document_system

from devdocs.canonical_sources import readme
from devdocs.canonical_sources.docs.api import descriptors as descriptor_api_doc
from devdocs.canonical_sources.docs.api import information as information_api_doc
from devdocs.canonical_sources.docs.api import realization as realization_api_doc
from devdocs.canonical_sources.docs.api import semantic_view as semantic_view_api_doc
from devdocs.canonical_sources.docs.api import shikumi as shikumi_api_doc
from devdocs.canonical_sources.docs.api import standard as standard_api_doc
from devdocs.canonical_sources.docs.api import structure as structure_api_doc
from devdocs.canonical_sources.docs.api import validation as validation_api_doc
from devdocs.canonical_sources.docs.guides import (
    descriptor_authoring as descriptor_authoring_doc,
)
from devdocs.canonical_sources.docs.guides import getting_started as getting_started_doc
from devdocs.canonical_sources.docs.guides import project_layout as project_layout_doc
from devdocs.canonical_sources.examples.structure_showcase import (
    canonical as structure_showcase_doc,
)

ROOT = Path(__file__).resolve().parents[1]


def _test_target_value(module, subject: type[object], binding_name: str) -> str:
    result = document_system.validate(module, placement=())
    assert result.is_valid, result.diagnostics
    item = next(entity for entity in result.view.entities if entity.subject is subject)
    values = [
        value
        for value in item.values(DocumentField)
        if isinstance(value, FieldValue) and value.binding_name == binding_name
    ]
    assert len(values) == 1
    assert values[0].presentation is FieldPresentation.TEST_TARGET
    assert isinstance(values[0].value, str)
    return cleandoc(values[0].value)


def _execute(code: str, name: str) -> dict[str, object]:
    namespace: dict[str, object] = {}
    exec(compile(code, name, "exec"), namespace, namespace)  # noqa: S102 - trusted in-test source is executed intentionally
    return namespace


def _execute_bash(code: str, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    pythonpath = [str(ROOT / "src"), str(ROOT / "examples"), str(ROOT)]
    if env.get("PYTHONPATH"):
        pythonpath.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath)
    return subprocess.run(
        ["bash", "-euo", "pipefail", "-c", code],
        cwd=tmp_path,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_readme_quickstart_code_executes() -> None:
    code = _test_target_value(readme, readme.README.QUICKSTART, "quickstart_code")
    namespace = _execute(code, "<README quickstart>")
    assert namespace["docs"].validate(namespace["Overview"]).is_valid


def test_getting_started_complete_example_executes() -> None:
    code = _test_target_value(
        getting_started_doc,
        getting_started_doc.GUIDE.COMPLETE_EXAMPLE,
        "complete_example",
    )
    namespace = _execute(code, "<Getting Started>")
    assert namespace["markdown"] == "# Overview\n"


def test_project_layout_validate_command_executes(tmp_path: Path) -> None:
    code = _test_target_value(
        project_layout_doc, project_layout_doc.GUIDE.CLI, "validate_command"
    )
    completed = _execute_bash(code, tmp_path)
    assert completed.returncode == 0, completed.stderr
    assert "valid" in completed.stdout.lower()


def test_structure_showcase_readme_code_executes() -> None:
    code = _test_target_value(
        structure_showcase_doc,
        structure_showcase_doc.EXAMPLE.TRY,
        "try_code",
    )
    namespace = _execute(code, "<structure showcase README>")
    assert namespace["valid_result"].is_valid
    assert not namespace["invalid_result"].is_valid


def test_descriptor_authoring_decorator_code_executes() -> None:
    code = _test_target_value(
        descriptor_authoring_doc,
        descriptor_authoring_doc.GUIDE.SECTION_001,
        "decorator_code",
    )
    _execute(code, "<descriptor authoring: decorator>")


def test_descriptor_authoring_parameterized_code_executes() -> None:
    code = _test_target_value(
        descriptor_authoring_doc,
        descriptor_authoring_doc.GUIDE.SECTION_002,
        "parameterized_code",
    )
    _execute(code, "<descriptor authoring: parameterized decorator>")


def test_descriptor_authoring_binding_code_executes() -> None:
    code = _test_target_value(
        descriptor_authoring_doc,
        descriptor_authoring_doc.GUIDE.SECTION_003,
        "binding_code",
    )
    _execute(code, "<descriptor authoring: class binding>")


def test_descriptor_authoring_rule_code_executes() -> None:
    code = _test_target_value(
        descriptor_authoring_doc,
        descriptor_authoring_doc.GUIDE.SECTION_004,
        "rule_code",
    )
    namespace = _execute(code, "<descriptor authoring: use rule>")
    assert namespace["result"].is_valid


def test_standard_assignment_api_example_executes() -> None:
    code = _test_target_value(
        standard_api_doc,
        standard_api_doc.API_REFERENCE_PART.TITLE_76.TITLE_77,
        "assignment_example",
    )
    _execute(code, "<Descriptor API: assignment>")


def test_standard_decorator_api_example_executes() -> None:
    code = _test_target_value(
        standard_api_doc,
        standard_api_doc.API_REFERENCE_PART.TITLE_76.TITLE_78,
        "decorator_example",
    )
    _execute(code, "<Descriptor API: decorator>")


def test_standard_docstring_api_example_executes() -> None:
    code = _test_target_value(
        standard_api_doc,
        standard_api_doc.API_REFERENCE_PART.TITLE_76.TITLE_79A,
        "docstring_example",
    )
    _execute(code, "<Descriptor API: docstring>")


def test_information_attachment_api_example_executes() -> None:
    code = _test_target_value(
        information_api_doc,
        information_api_doc.API_REFERENCE_PART.TITLE_4.TITLE_10,
        "attachment_example",
    )
    _execute(code, "<Information API: attachment>")


def test_descriptor_class_binding_api_example_executes() -> None:
    code = _test_target_value(
        descriptor_api_doc,
        descriptor_api_doc.API_REFERENCE_PART.TITLE_20.TITLE_21,
        "class_binding_example",
    )
    _execute(code, "<Descriptor API: class binding>")


def test_information_type_rule_api_example_executes() -> None:
    code = _test_target_value(
        standard_api_doc,
        standard_api_doc.API_REFERENCE_PART.TITLE_76.TITLE_82,
        "information_type_rule_example",
    )
    _execute(code, "<Descriptor API: information type rule>")


def test_structure_resolution_api_example_executes() -> None:
    code = _test_target_value(
        structure_api_doc,
        structure_api_doc.API_REFERENCE_PART.TITLE_22.TITLE_29,
        "resolution_example",
    )
    _execute(code, "<Structure API: resolution>")


def test_logical_structure_api_example_executes() -> None:
    code = _test_target_value(
        structure_api_doc,
        structure_api_doc.API_REFERENCE_PART.TITLE_22.TITLE_31,
        "logical_structure_example",
    )
    _execute(code, "<Structure API: logical structure>")


def test_advanced_structure_api_example_executes() -> None:
    code = _test_target_value(
        structure_api_doc,
        structure_api_doc.API_REFERENCE_PART.TITLE_22.TITLE_31,
        "advanced_structure_example",
    )
    _execute(code, "<Structure API: recursive and grouped structure>")


def test_semantic_view_query_api_example_executes() -> None:
    code = _test_target_value(
        semantic_view_api_doc,
        semantic_view_api_doc.API_REFERENCE_PART.TITLE_34.TITLE_42,
        "query_example",
    )
    _execute(code, "<Semantic View API: query>")


def test_shikumi_composition_api_example_executes() -> None:
    code = _test_target_value(
        shikumi_api_doc,
        shikumi_api_doc.API_REFERENCE_PART.TITLE_49.TITLE_52,
        "composition_example",
    )
    _execute(code, "<Shikumi API: composition>")


def test_validator_api_example_executes() -> None:
    code = _test_target_value(
        validation_api_doc,
        validation_api_doc.API_REFERENCE_PART.TITLE_55.TITLE_59,
        "validator_example",
    )
    _execute(code, "<Validation API: validator>")


def test_structure_check_api_example_executes() -> None:
    code = _test_target_value(
        validation_api_doc,
        validation_api_doc.API_REFERENCE_PART.TITLE_55.TITLE_61B,
        "structure_check_example",
    )
    _execute(code, "<Validation API: structure check>")


def test_realizer_api_example_executes() -> None:
    code = _test_target_value(
        realization_api_doc,
        realization_api_doc.API_REFERENCE_PART.TITLE_64.TITLE_66,
        "realizer_example",
    )
    _execute(code, "<Realization API: realizer>")


def test_published_documents_preserve_all_test_targets_verbatim() -> None:
    from devdocs.canonical_sources.devdocs import readme as devdocs_readme

    documents = (
        (readme, readme.README, Path("README.md")),
        (devdocs_readme, devdocs_readme.DEVDOCS_README, Path("devdocs/README.md")),
        (
            getting_started_doc,
            getting_started_doc.GUIDE,
            Path("docs/guides/getting-started.md"),
        ),
        (
            descriptor_authoring_doc,
            descriptor_authoring_doc.GUIDE,
            Path("docs/guides/descriptor-authoring.md"),
        ),
        (
            project_layout_doc,
            project_layout_doc.GUIDE,
            Path("docs/guides/project-layout.md"),
        ),
        (
            information_api_doc,
            information_api_doc.API_REFERENCE_PART,
            Path("docs/api/information.md"),
        ),
        (
            descriptor_api_doc,
            descriptor_api_doc.API_REFERENCE_PART,
            Path("docs/api/descriptors.md"),
        ),
        (
            structure_api_doc,
            structure_api_doc.API_REFERENCE_PART,
            Path("docs/api/structure.md"),
        ),
        (
            semantic_view_api_doc,
            semantic_view_api_doc.API_REFERENCE_PART,
            Path("docs/api/semantic-view.md"),
        ),
        (
            shikumi_api_doc,
            shikumi_api_doc.API_REFERENCE_PART,
            Path("docs/api/shikumi.md"),
        ),
        (
            validation_api_doc,
            validation_api_doc.API_REFERENCE_PART,
            Path("docs/api/validation.md"),
        ),
        (
            realization_api_doc,
            realization_api_doc.API_REFERENCE_PART,
            Path("docs/api/realization.md"),
        ),
        (
            standard_api_doc,
            standard_api_doc.API_REFERENCE_PART,
            Path("docs/api/standard.md"),
        ),
        (
            structure_showcase_doc,
            structure_showcase_doc.EXAMPLE,
            Path("examples/structure_showcase/README.md"),
        ),
    )

    for module, root, published_path in documents:
        result = document_system.validate(module, placement=())
        assert result.is_valid, (module.__name__, result.diagnostics)
        published = published_path.read_text(encoding="utf-8")
        fenced_blocks = tuple(
            block.rstrip("\n")
            for block in re.findall(
                r"```[^\n]*\n(.*?)\n```", published, flags=re.DOTALL
            )
        )
        target_values = [
            cleandoc(value.value)
            for item in result.view.items
            if item.node.path[:1] == result.view.item(root).node.path[:1]
            for value in item.values(DocumentField)
            if isinstance(value, FieldValue)
            and value.presentation is FieldPresentation.TEST_TARGET
            and isinstance(value.value, str)
        ]
        assert target_values, published_path
        for code in target_values:
            assert code in published, (published_path, code[:80])
            assert code in fenced_blocks, (published_path, code[:80])
