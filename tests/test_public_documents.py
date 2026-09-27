from pathlib import Path


def test_public_document_layout() -> None:
    root = Path('.')

    assert (root / 'README.md').is_file()
    assert (root / 'CHANGELOG.md').is_file()
    assert (root / 'STATUS.md').is_file()
    assert (root / 'devdocs' / 'README.md').is_file()
    assert not (root / 'DOCUMENTATION_WORKFLOW.md').exists()
    assert (root / 'docs' / 'glossary.md').is_file()
    assert (root / 'docs' / 'api' / 'INDEX.md').is_file()
    assert (root / 'docs' / 'api' / 'information.md').is_file()
    assert (root / 'docs' / 'api' / 'cli.md').is_file()
    assert (root / 'docs' / 'api' / 'standard.md').is_file()
    assert (root / 'docs' / 'specification' / 'INDEX.md').is_file()
    assert (root / 'docs' / 'specification' / 'core.md').is_file()
    assert (root / 'docs' / 'specification' / 'cli.md').is_file()
    assert (root / 'docs' / 'guides' / 'INDEX.md').is_file()
    assert (root / 'docs' / 'guides' / 'getting-started.md').is_file()
    assert (root / 'docs' / 'guides' / 'descriptor-authoring.md').is_file()
    assert (root / 'docs' / 'guides' / 'project-layout.md').is_file()

    assert (root / "examples" / "structure_showcase" / "README.md").is_file()
    for removed in ("architecture", "structured_docs", "web_api", "structure_from_body"):
        assert not (root / "examples" / removed).exists()

    assert not (root / 'docs' / 'api-reference.md').exists()
    assert not (root / 'README_DRAFT.md').exists()
    assert not (root / 'GLOSSARY.md').exists()
    assert not (root / 'API_REFERENCE.md').exists()
    assert not (root / 'DISTRIBUTION_GUIDE.md').exists()
    assert not (root / 'docs' / 'distribution-guide.md').exists()


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


def test_committed_canonical_document_layout() -> None:
    root = Path("devdocs/canonical_documents")
    expected = (
        Path("README.md"),
        Path("CHANGELOG.md"),
        Path("STATUS.md"),
        Path("devdocs/README.md"),
        Path("docs/glossary.md"),
        Path("docs/guides/INDEX.md"),
        Path("docs/guides/getting-started.md"),
        Path("docs/guides/descriptor-authoring.md"),
        Path("docs/guides/project-layout.md"),
        Path("docs/api/INDEX.md"),
        Path("docs/api/information.md"),
        Path("docs/api/descriptors.md"),
        Path("docs/api/structure.md"),
        Path("docs/api/semantic-view.md"),
        Path("docs/api/shikumi.md"),
        Path("docs/api/validation.md"),
        Path("docs/api/realization.md"),
        Path("docs/api/standard.md"),
        Path("docs/api/errors.md"),
        Path("docs/api/cli.md"),
        Path("docs/specification/INDEX.md"),
        Path("docs/specification/core.md"),
        Path("docs/specification/description.md"),
        Path("docs/specification/structure.md"),
        Path("docs/specification/validation.md"),
        Path("docs/specification/realization.md"),
        Path("docs/specification/public-api.md"),
        Path("docs/specification/cli.md"),
        Path("examples/structure_showcase/README.md"),
    )

    for relative in expected:
        path = root / relative
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        assert "この文書は `shikumi-devdoc` で生成した日本語 canonical document です。" in text
        if text.startswith("<!-- shikumi-devdoc:translation-metadata\n"):
            assert '"publication": "omit-this-comment"' in text


def test_shikumi_devdoc_is_a_repository_development_dependency_only() -> None:
    import tomllib

    with Path("pyproject.toml").open("rb") as stream:
        pyproject = tomllib.load(stream)

    assert pyproject["dependency-groups"]["docs"] == ["shikumi-devdoc>=0.3.0"]
    assert "shikumi-devdoc" not in " ".join(pyproject["project"].get("dependencies", ()))
