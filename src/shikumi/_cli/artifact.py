"""Serialization and filesystem writing for realized CLI artifacts."""

from __future__ import annotations

import json
from pathlib import Path

from .types import ArtifactWrite, CLIError


def write_artifact(artifact: object, output: str) -> ArtifactWrite:
    path = Path(output)
    try:
        if isinstance(artifact, str):
            _ = path.write_text(artifact, encoding="utf-8")
            return ArtifactWrite(path=path, kind="text")
        if isinstance(artifact, bytes):
            _ = path.write_bytes(artifact)
            return ArtifactWrite(path=path, kind="binary")
        if isinstance(artifact, bytearray):
            _ = path.write_bytes(bytes(artifact))
            return ArtifactWrite(path=path, kind="binary")
        if isinstance(artifact, memoryview):
            _ = path.write_bytes(artifact.tobytes())
            return ArtifactWrite(path=path, kind="binary")

        encoded = (
            json.dumps(
                artifact,
                ensure_ascii=False,
                indent=2,
                allow_nan=False,
            )
            + "\n"
        )
        _ = path.write_text(encoded, encoding="utf-8")
        return ArtifactWrite(path=path, kind="json")
    except (TypeError, ValueError) as exc:
        raise CLIError(
            "artifact_error",
            "realizer returned an artifact that the CLI cannot write; "
            "return str, bytes, or a JSON-serializable value",
        ) from exc
    except OSError as exc:
        raise CLIError(
            "output_error",
            f"could not write artifact to {str(path)!r}: {exc}",
        ) from exc
