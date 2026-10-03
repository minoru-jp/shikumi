from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_distribution_metadata_uses_spdx_license_expression() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]

    assert project["license"] == "MIT"
    assert project["license-files"] == ["LICENSE"]


def test_project_urls_point_to_the_public_repository() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert data["project"]["urls"] == {
        "Homepage": "https://github.com/minoru-jp/shikumi",
        "Repository": "https://github.com/minoru-jp/shikumi",
        "Documentation": "https://github.com/minoru-jp/shikumi/tree/main/docs",
        "Issues": "https://github.com/minoru-jp/shikumi/issues",
    }


def test_wheel_embeds_public_documentation_but_not_repository_internals() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    wheel = data["tool"]["hatch"]["build"]["targets"]["wheel"]

    assert wheel["packages"] == ["src/shikumi"]
    assert wheel["force-include"] == {
        "README.md": "shikumi/_docs/README.md",
        "CHANGELOG.md": "shikumi/_docs/CHANGELOG.md",
        "STATUS.md": "shikumi/_docs/STATUS.md",
        "docs": "shikumi/_docs",
        "examples": "shikumi/_examples",
    }


def test_sdist_is_complete_release_source_with_narrow_repository_exclusions() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    sdist = data["tool"]["hatch"]["build"]["targets"]["sdist"]

    assert "include" not in sdist
    assert set(sdist["exclude"]) == {"/.github"}


def test_examples_are_reference_sources_not_a_public_top_level_package() -> None:
    assert Path("examples").is_dir()
    assert not Path("src/shikumi_examples").exists()
    assert not list(Path("examples").glob("*/__main__.py"))


def test_0_2_4_keeps_the_beta_release_contract() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]

    assert project["version"] == "0.2.4"
    assert "Development Status :: 4 - Beta" in project["classifiers"]
    assert "Programming Language :: Python :: 3.14" in project["classifiers"]
    assert "Development Status :: 3 - Alpha" not in project["classifiers"]


def test_readme_navigation_is_safe_when_rendered_on_pypi() -> None:
    import re

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    targets = re.findall(r"\[[^\]]*\]\(([^)]+)\)", readme)

    assert targets
    assert all(
        target.startswith(("https://", "http://", "mailto:", "#")) for target in targets
    )
    assert any(
        target.startswith("https://github.com/minoru-jp/shikumi/") for target in targets
    )
