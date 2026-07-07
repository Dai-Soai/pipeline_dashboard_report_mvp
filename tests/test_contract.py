import pytest

from pipeline_dashboard_report.contract import (
    build_artifact_summary,
    build_artifact_type_stats,
    build_dashboard_report,
    build_dashboard_status_summary,
)


def test_build_artifact_summary_success():
    artifact = {
        "artifact_type": "delivery_report",
        "summary": {
            "total": 2,
            "delivered": 2,
            "failed": 0,
        },
    }

    summary = build_artifact_summary(
        artifact=artifact,
        source_path="samples/delivery_report.json",
    )

    assert summary.artifact_type == "delivery_report"
    assert summary.source_path == "samples/delivery_report.json"
    assert summary.status == "UNKNOWN"
    assert summary.total_items == 2


def test_build_artifact_summary_rejects_non_object():
    with pytest.raises(ValueError, match="artifact"):
        build_artifact_summary(
            artifact=[],
            source_path="bad.json",
        )


def test_build_artifact_summary_rejects_missing_artifact_type():
    with pytest.raises(ValueError, match="artifact_type"):
        build_artifact_summary(
            artifact={},
            source_path="missing.json",
        )


def test_build_dashboard_report_success():
    artifact = {
        "artifact_type": "delivery_report",
        "status": "SUCCESS",
        "summary": {
            "total": 2,
        },
    }

    item = build_artifact_summary(
        artifact=artifact,
        source_path="samples/delivery_report.json",
    )

    report = build_dashboard_report(
        report_id="dashboard-001",
        artifacts=[item],
    )

    assert report.report_id == "dashboard-001"
    assert report.artifact_count == 1
    assert report.summary["success"] == 1
    assert report.summary["unknown"] == 0
    assert report.artifacts[0].artifact_type == "delivery_report"
    assert report.generated_at
