from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_json_artifact(path: str | Path) -> dict[str, Any]:
    artifact_path = Path(path)

    if not artifact_path.exists():
        raise FileNotFoundError(f"Artifact file not found: {artifact_path}")

    if not artifact_path.is_file():
        raise ValueError(f"Artifact path is not a file: {artifact_path}")

    try:
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON artifact: {artifact_path}") from exc

    if not isinstance(payload, dict):
        raise ValueError("JSON artifact must be an object")

    return payload


def read_jsonl_artifact(path: str | Path) -> list[dict[str, Any]]:
    artifact_path = Path(path)

    if not artifact_path.exists():
        raise FileNotFoundError(f"Artifact file not found: {artifact_path}")

    if not artifact_path.is_file():
        raise ValueError(f"Artifact path is not a file: {artifact_path}")

    records: list[dict[str, Any]] = []

    for line_number, line in enumerate(
        artifact_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSONL record at line {line_number}: {artifact_path}"
            ) from exc

        if not isinstance(payload, dict):
            raise ValueError(f"JSONL record at line {line_number} must be an object")

        records.append(payload)

    return records
