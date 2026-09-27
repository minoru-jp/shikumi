from __future__ import annotations

import argparse
import tarfile
import zipfile
from pathlib import Path


REQUIRED_WHEEL_SUFFIXES = {
    "shikumi/__init__.py",
    "shikumi/py.typed",
    "shikumi/_docs/README.md",
    "shikumi/_docs/CHANGELOG.md",
    "shikumi/_docs/STATUS.md",
    "shikumi/_docs/glossary.md",
    "shikumi/_docs/api/INDEX.md",
    "shikumi/_docs/api/information.md",
    "shikumi/_docs/specification/INDEX.md",
    "shikumi/_docs/specification/core.md",
    "shikumi/_docs/guides/INDEX.md",
    "shikumi/_docs/guides/getting-started.md",
    "shikumi/_docs/guides/descriptor-authoring.md",
    "shikumi/_docs/guides/project-layout.md",
    "shikumi/_examples/structure_showcase/README.md",
    "shikumi/_examples/structure_showcase/specification.py",
    "shikumi/_examples/structure_showcase/valid/combined/required/__init__.py",
    "shikumi/_examples/structure_showcase/invalid/group_both/mode/remote/__init__.py",
}


WHEEL_FORBIDDEN_PARTS = {
    "_internal",
    "tests",
    "__pycache__",
    "shikumi_examples",
    "devdocs",
    "scripts",
}
SDIST_FORBIDDEN_PARTS = {
    ".git",
    ".github",
    ".jj",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".pyright",
    ".ruff_cache",
    "build",
    "dist",
}


def _assert_no_forbidden_parts(
    names: list[str], *, archive: Path, forbidden_parts: set[str]
) -> None:
    bad = [name for name in names if forbidden_parts.intersection(Path(name).parts)]
    if bad:
        raise SystemExit(f"{archive.name}: forbidden paths found: {bad[:10]}")


def check_wheel(path: Path) -> None:
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()

    _assert_no_forbidden_parts(
        names, archive=path, forbidden_parts=WHEEL_FORBIDDEN_PARTS
    )
    missing = [suffix for suffix in REQUIRED_WHEEL_SUFFIXES if not any(name.endswith(suffix) for name in names)]
    if missing:
        raise SystemExit(f"{path.name}: required wheel files missing: {missing}")


def check_sdist(path: Path) -> None:
    with tarfile.open(path, "r:gz") as tf:
        names = tf.getnames()

    _assert_no_forbidden_parts(
        names, archive=path, forbidden_parts=SDIST_FORBIDDEN_PARTS
    )
    required_suffixes = {
        "README.md",
        "CHANGELOG.md",
        "STATUS.md",
        "LICENSE",
        "pyproject.toml",
        "docs/glossary.md",
        "docs/api/INDEX.md",
        "docs/api/information.md",
        "docs/specification/INDEX.md",
        "docs/specification/core.md",
        "docs/guides/INDEX.md",
        "docs/guides/getting-started.md",
        "docs/guides/descriptor-authoring.md",
        "docs/guides/project-layout.md",
        "examples/structure_showcase/README.md",
        "examples/structure_showcase/specification.py",
        "examples/structure_showcase/valid/combined/required/__init__.py",
        "examples/structure_showcase/invalid/group_both/mode/remote/__init__.py",
        "src/shikumi/__init__.py",
        "tests/test_packaging.py",
        "tests/test_devdocs.py",
        "devdocs/README.md",
        "devdocs/canonical_sources/changelog.py",
        "devdocs/canonical_sources/devdocs/readme.py",
        "devdocs/canonical_documents/CHANGELOG.md",
        "devdocs/config/notice.toml",
        "scripts/check_dist.py",
        "scripts/render_canonical_docs.py",
    }
    missing = [suffix for suffix in required_suffixes if not any(name.endswith(suffix) for name in names)]
    if missing:
        raise SystemExit(f"{path.name}: required sdist files missing: {missing}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Shikumi release archives.")
    parser.add_argument("dist_dir", nargs="?", default="dist", type=Path)
    args = parser.parse_args()

    wheels = sorted(args.dist_dir.glob("*.whl"))
    sdists = sorted(args.dist_dir.glob("*.tar.gz"))
    if len(wheels) != 1 or len(sdists) != 1:
        raise SystemExit(
            f"expected exactly one wheel and one sdist in {args.dist_dir}, "
            f"found {len(wheels)} wheel(s) and {len(sdists)} sdist(s)"
        )

    check_wheel(wheels[0])
    check_sdist(sdists[0])
    print(f"checked {wheels[0].name} and {sdists[0].name}")


if __name__ == "__main__":
    main()
