from pathlib import Path


def test_public_document_layout() -> None:
    root = Path('.')

    assert (root / 'README.md').is_file()
    assert (root / 'CHANGELOG.md').is_file()
    assert (root / 'DOCUMENTATION_WORKFLOW.md').is_file()
    assert (root / 'docs' / 'glossary.md').is_file()
    assert (root / 'docs' / 'api-reference.md').is_file()
    assert (root / 'docs' / 'distribution-guide.md').is_file()

    for example in ("architecture", "structured_docs", "web_api", "structure_from_body"):
        assert (root / "examples" / example / "README.md").is_file()

    assert not (root / 'README_DRAFT.md').exists()
    assert not (root / 'GLOSSARY.md').exists()
    assert not (root / 'API_REFERENCE.md').exists()
    assert not (root / 'DISTRIBUTION_GUIDE.md').exists()


def test_pyproject_uses_public_readme() -> None:
    pyproject = Path('pyproject.toml').read_text()
    assert 'readme = "README.md"' in pyproject


def test_public_readme_version_matches_pyproject() -> None:
    import tomllib

    root = Path('.')
    with (root / "pyproject.toml").open("rb") as stream:
        project_version = tomllib.load(stream)["project"]["version"]

    readme = (root / "README.md").read_text(encoding="utf-8")
    assert f"Current version: `{project_version}`." in readme


def test_committed_japanese_document_intermediate_layout() -> None:
    root = Path("_internal/document_build/ja")
    expected = (
        Path("README.md"),
        Path("CHANGELOG.md"),
        Path("DOCUMENTATION_WORKFLOW.md"),
        Path("docs/glossary.md"),
        Path("docs/api-reference.md"),
        Path("docs/distribution-guide.md"),
        Path("examples/architecture/README.md"),
        Path("examples/structured_docs/README.md"),
        Path("examples/web_api/README.md"),
        Path("examples/structure_from_body/README.md"),
    )

    for relative in expected:
        path = root / relative
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        assert text.startswith("<!-- shikumi-devdoc:translation-metadata\n")
        assert "この文書は自動生成された翻訳元の中間文書です。" in text


def test_shikumi_devdoc_is_a_repository_development_dependency_only() -> None:
    import tomllib

    with Path("pyproject.toml").open("rb") as stream:
        pyproject = tomllib.load(stream)

    assert pyproject["dependency-groups"]["docs"] == ["shikumi-devdoc==0.1.0"]
    assert "shikumi-devdoc" not in " ".join(pyproject["project"].get("dependencies", ()))
