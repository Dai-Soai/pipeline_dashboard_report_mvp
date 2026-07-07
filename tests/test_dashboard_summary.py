from pipeline_dashboard_report.contract import (
    ArtifactSummary,
    build_artifact_type_stats,
    build_dashboard_status_summary,
)


def test_build_dashboard_status_summary():
    artifacts = [
        ArtifactSummary("delivery_report", "a.json", "SUCCESS", 2),
        ArtifactSummary("execution_report", "b.json", "FAILED", 1),
        ArtifactSummary("notification_report", "c.json", "WARNING", 3),
        ArtifactSummary("audit_log", "d.jsonl", "UNKNOWN", 4),
    ]

    summary = build_dashboard_status_summary(artifacts)

    assert summary["success"] == 1
    assert summary["failed"] == 1
    assert summary["warning"] == 1
    assert summary["unknown"] == 1


def test_build_dashboard_status_summary_maps_delivered_to_success():
    artifacts = [
        ArtifactSummary("delivery_report", "a.json", "DELIVERED", 2),
        ArtifactSummary("audit_log", "b.jsonl", "RECORDED", 1),
    ]

    summary = build_dashboard_status_summary(artifacts)

    assert summary["success"] == 2
    assert summary["failed"] == 0


def test_build_artifact_type_stats():
    artifacts = [
        ArtifactSummary("delivery_report", "a.json", "SUCCESS", 2),
        ArtifactSummary("delivery_report", "b.json", "SUCCESS", 3),
        ArtifactSummary("execution_report", "c.json", "FAILED", 1),
    ]

    stats = build_artifact_type_stats(artifacts)

    assert stats["delivery_report"] == 2
    assert stats["execution_report"] == 1
