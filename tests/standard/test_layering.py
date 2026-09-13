from __future__ import annotations

from pathlib import Path

import shikumi


def test_core_modules_do_not_import_standard_layer() -> None:
    core_dir = Path(shikumi.__file__).parent
    for path in core_dir.glob("*.py"):
        source = path.read_text(encoding="utf-8")
        assert "shikumi.standard" not in source
        assert ".standard" not in source
