import json

import pytest

from pipeline_dashboard_report.reader import (
    read_json_artifact,
    read_jsonl_artifact,
)


def test_read_json_artifact_success(tmp_path):
    path = tmp_path / "delivery_report.json"
    path.write_text(
        json.dumps(
            {
                "artifact_type": "delivery_report",
                "summary": {"total": 2},
            }
        ),
        encoding="utf-8",
    )

    payload = read_json_artifact(path)

    assert payload["artifact_type"] == "delivery_report"
    assert payload["summary"]["total"] == 2


def test_read_json_artifact_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_json_artifact(tmp_path / "missing.json")


def test_read_json_artifact_rejects_invalid_json(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{bad json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        read_json_artifact(path)


def test_read_json_artifact_rejects_non_object(tmp_path):
    path = tmp_path / "array.json"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="object"):
        read_json_artifact(path)


def test_read_jsonl_artifact_success(tmp_path):
    path = tmp_path / "audit_log.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "event_id": "audit-001",
                        "artifact_type": "delivery_report",
                    }
                ),
                json.dumps(
                    {
                        "event_id": "audit-002",
                        "artifact_type": "execution_report",
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )

    records = read_jsonl_artifact(path)

    assert len(records) == 2
    assert records[0]["artifact_type"] == "delivery_report"
    assert records[1]["artifact_type"] == "execution_report"


def test_read_jsonl_artifact_rejects_invalid_line(tmp_path):
    path = tmp_path / "audit_log.jsonl"
    path.write_text('{"ok": true}\n{bad json', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSONL record"):
        read_jsonl_artifact(path)


def test_read_jsonl_artifact_rejects_non_object_record(tmp_path):
    path = tmp_path / "audit_log.jsonl"
    path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError, match="must be an object"):
        read_jsonl_artifact(path)
