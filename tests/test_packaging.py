from __future__ import annotations

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_distribution_metadata_uses_spdx_license_expression() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]

    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE"]


def test_wheel_embeds_public_documentation_but_not_repository_internals() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    wheel = data["tool"]["hatch"]["build"]["targets"]["wheel"]

    assert wheel["packages"] == ["src/shikumi"]
    assert wheel["force-include"] == {
        "README.md": "shikumi/_docs/README.md",
        "CHANGELOG.md": "shikumi/_docs/CHANGELOG.md",
        "docs": "shikumi/_docs",
        "examples": "shikumi/_examples",
    }


def test_sdist_contains_public_sources_and_excludes_internal_development_trees() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    include = set(data["tool"]["hatch"]["build"]["targets"]["sdist"]["include"])

    assert "/src/shikumi" in include
    assert "/examples" in include
    assert "/docs" in include
    assert "/CHANGELOG.md" in include
    assert "/_internal" not in include
    assert "/tests" not in include


def test_examples_are_reference_sources_not_a_public_top_level_package() -> None:
    assert Path("examples").is_dir()
    assert not Path("src/shikumi_examples").exists()
    assert not list(Path("examples").glob("*/__main__.py"))
