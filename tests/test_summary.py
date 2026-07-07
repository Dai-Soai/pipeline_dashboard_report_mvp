from pipeline_dashboard_report.summary import (
    build_dashboard_from_artifacts,
    build_summaries_from_artifacts,
)


def test_build_summaries_from_artifacts():
    artifacts = [
        (
            "samples/delivery_report.json",
            {
                "artifact_type": "delivery_report",
                "summary": {"total": 2},
            },
        ),
        (
            "samples/execution_report.json",
            {
                "artifact_type": "execution_report",
                "summary": {"total": 3},
                "status": "SUCCESS",
            },
        ),
    ]

    summaries = build_summaries_from_artifacts(artifacts)

    assert len(summaries) == 2
    assert summaries[0].artifact_type == "delivery_report"
    assert summaries[0].total_items == 2
    assert summaries[1].artifact_type == "execution_report"
    assert summaries[1].status == "SUCCESS"


def test_build_dashboard_from_artifacts():
    artifacts = [
        (
            "samples/delivery_report.json",
            {
                "artifact_type": "delivery_report",
                "summary": {"total": 2},
            },
        )
    ]

    report = build_dashboard_from_artifacts(artifacts)

    assert report.report_id.startswith("dashboard-")
    assert report.artifact_count == 1
    assert report.artifacts[0].artifact_type == "delivery_report"
    assert report.generated_at
