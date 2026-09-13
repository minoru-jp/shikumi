from __future__ import annotations

import json
import sys
from pathlib import Path

from shikumi.cli import main


def _write_fixture(tmp_path: Path) -> str:
    package = tmp_path / "cli_fixture"
    package.mkdir()
    (package / "__init__.py").write_text(
        "\n".join(
            [
                "from shikumi import Diagnostic, InformationType, RealizationCheck, Realizer, Shikumi, StructuralKind, StructureElement, StructureSpecification, validator",
                "from shikumi.standard import assignment",
                "Title = InformationType('title', str)",
                "title = assignment(Title)",
                "@validator(focus=StructuralKind.ENTITY)",
                "def require_title(view):",
                "    if not view.focused.has(Title):",
                "        yield Diagnostic('title is required', code='title.required')",
                "spec = Shikumi(information_types=[Title], validators=[require_title])",
                "class Good:",
                "    title @= 'Good title'",
                "class Bad:",
                "    pass",
                "class TextRealizer(Realizer[str]):",
                "    def realize(self, view):",
                "        values = view.focused.values(Title)",
                "        return values[0] if values else 'missing'",
                "text = TextRealizer()",
                "class JsonRealizer(Realizer[dict]):",
                "    def realize(self, view):",
                "        return {'name': view.focused.node.name}",
                "json_realizer = JsonRealizer()",
                "class UnsupportedRealizer(Realizer[object]):",
                "    def realize(self, view):",
                "        return object()",
                "unsupported = UnsupportedRealizer()",
                "class NeverRealizer(Realizer[str]):",
                "    def check(self, view):",
                "        return RealizationCheck(view, (Diagnostic('cannot realize this view', code='realizer.never'),))",
                "    def realize(self, view):",
                "        return 'never'",
                "never = NeverRealizer()",
                "module_structure = StructureSpecification([",
                "    StructureElement((), StructuralKind.MODULE),",
                "    StructureElement(('Item',), StructuralKind.ENTITY),",
                "])",
            ]
        ),
        encoding="utf-8",
    )
    (package / "reference_module.py").write_text("from cli_fixture import title\nclass Item:\n    title @= 'Item'\n", encoding="utf-8")
    (package / "candidate_module.py").write_text("from cli_fixture import title\nclass Item:\n    title @= 'Item'\n", encoding="utf-8")
    (package / "wrong_module.py").write_text("from cli_fixture import title\nclass Other:\n    title @= 'Other'\n", encoding="utf-8")
    return "cli_fixture"


def _drop_modules(prefix: str) -> None:
    for name in tuple(sys.modules):
        if name == prefix or name.startswith(prefix + "."):
            sys.modules.pop(name, None)


def test_validate_text_success(tmp_path, monkeypatch, capsys) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        code = main(
            [
                "validate",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}:Good",
            ]
        )
        output = capsys.readouterr().out
        assert code == 0
        assert "Validation succeeded" in output
        assert "Diagnostics: 0 error, 0 warning, 0 info" in output
    finally:
        _drop_modules(package)


def test_validate_json_failure_is_structured(tmp_path, monkeypatch, capsys) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        code = main(
            [
                "validate",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}:Bad",
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 1
        assert payload["format_version"] == 1
        assert payload["command"] == "validate"
        assert payload["ok"] is False
        assert payload["diagnostic_counts"] == {
            "error": 1,
            "warning": 0,
            "info": 0,
        }
        assert payload["diagnostics"][0]["code"] == "title.required"
        assert payload["diagnostics"][0]["subject"].endswith("Bad")
    finally:
        _drop_modules(package)


def test_realize_writes_text_artifact_and_json_status(
    tmp_path, monkeypatch, capsys
) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    output = tmp_path / "artifact.txt"
    try:
        code = main(
            [
                "realize",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}:Good",
                "--realizer",
                f"{package}:text",
                "--output",
                str(output),
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 0
        assert output.read_text(encoding="utf-8") == "Good title"
        assert payload["command"] == "realize"
        assert payload["ok"] is True
        assert payload["artifact"] == {
            "output": str(output),
            "kind": "text",
        }
    finally:
        _drop_modules(package)


def test_realize_serializes_json_compatible_artifact(
    tmp_path, monkeypatch, capsys
) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    output = tmp_path / "artifact.json"
    try:
        code = main(
            [
                "realize",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}:Good",
                "--realizer",
                f"{package}:json_realizer",
                "--output",
                str(output),
            ]
        )
        capsys.readouterr()
        assert code == 0
        assert json.loads(output.read_text(encoding="utf-8")) == {"name": "Good"}
    finally:
        _drop_modules(package)


def test_realize_reports_unsupported_artifact_in_json(
    tmp_path, monkeypatch, capsys
) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    output = tmp_path / "artifact.out"
    try:
        code = main(
            [
                "realize",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}:Good",
                "--realizer",
                f"{package}:unsupported",
                "--output",
                str(output),
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 1
        assert payload["ok"] is False
        assert payload["error"]["type"] == "artifact_error"
        assert not output.exists()
    finally:
        _drop_modules(package)


def test_reference_error_uses_requested_response_format(capsys) -> None:
    code = main(
        [
            "validate",
            "--shikumi",
            "missing_module:spec",
            "--body",
            "missing_body",
            "--format",
            "json",
        ]
    )
    payload = json.loads(capsys.readouterr().out)
    assert code == 1
    assert payload["ok"] is False
    assert payload["error"]["type"] == "import_error"


def test_realize_wraps_interpretation_error_for_json(tmp_path, monkeypatch, capsys) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    output = tmp_path / "artifact.txt"
    try:
        code = main(
            [
                "realize",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}:text",
                "--realizer",
                f"{package}:text",
                "--output",
                str(output),
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 1
        assert payload["error"]["type"] == "interpretation_error"
    finally:
        _drop_modules(package)


def test_validate_module_requires_explicit_placement(tmp_path, monkeypatch, capsys) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        code = main(
            [
                "validate",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}.candidate_module",
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 1
        assert payload["error"]["type"] == "placement_required"
    finally:
        _drop_modules(package)


def test_validate_uses_explicit_structure_specification(tmp_path, monkeypatch, capsys) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        code = main(
            [
                "validate",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}.candidate_module",
                "--at",
                ".",
                "--structure-spec",
                f"{package}:module_structure",
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 0
        assert payload["ok"] is True
        assert payload["structure"] == {
            "mode": "explicit",
            "reference": f"{package}:module_structure",
            "ok": True,
            "placement": ".",
        }
    finally:
        _drop_modules(package)


def test_validate_can_derive_structure_from_description_body(tmp_path, monkeypatch, capsys) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        code = main(
            [
                "validate",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}.candidate_module",
                "--at",
                ".",
                "--structure-from",
                f"{package}.reference_module",
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 0
        assert payload["structure"]["mode"] == "derived"
        assert payload["structure"]["reference"] == f"{package}.reference_module"
        assert payload["structure"]["ok"] is True
    finally:
        _drop_modules(package)


def test_explicit_structure_reference_does_not_fall_back_when_missing(
    tmp_path, monkeypatch, capsys
) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        code = main(
            [
                "validate",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}:Good",
                "--structure-spec",
                f"{package}:missing_structure",
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 1
        assert payload["error"]["type"] == "reference_error"
    finally:
        _drop_modules(package)


def test_validate_can_query_realizer_without_realizing(tmp_path, monkeypatch, capsys) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        code = main(
            [
                "validate",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}:Good",
                "--realizer",
                f"{package}:never",
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 1
        assert payload["diagnostic_counts"]["error"] == 0
        assert payload["realization"]["ok"] is False
        assert payload["realization"]["diagnostics"][0]["code"] == "realizer.never"
    finally:
        _drop_modules(package)


def test_validate_reports_structural_mismatch_separately(tmp_path, monkeypatch, capsys) -> None:
    package = _write_fixture(tmp_path)
    monkeypatch.syspath_prepend(str(tmp_path))
    try:
        code = main(
            [
                "validate",
                "--shikumi",
                f"{package}:spec",
                "--body",
                f"{package}.wrong_module",
                "--at",
                ".",
                "--structure-spec",
                f"{package}:module_structure",
                "--format",
                "json",
            ]
        )
        payload = json.loads(capsys.readouterr().out)
        assert code == 1
        assert payload["structure"]["ok"] is False
        assert {item["code"] for item in payload["diagnostics"]} == {
            "structure.element.missing",
            "structure.element.unexpected",
        }
        assert payload["realization"] is None
    finally:
        _drop_modules(package)
