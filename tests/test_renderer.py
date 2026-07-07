from pipeline_dashboard_report.contract import (
    build_artifact_summary,
    build_dashboard_report,
)

from pipeline_dashboard_report.renderer import (
    render_dashboard_json,
    render_dashboard_markdown,
)


def build_report():
    artifact = build_artifact_summary(
        artifact={
            "artifact_type": "delivery_report",
            "summary": {
                "total": 2,
            },
        },
        source_path="samples/delivery_report.json",
    )

    return build_dashboard_report(
        report_id="dashboard-001",
        artifacts=[artifact],
    )


def test_render_dashboard_json():
    report = build_report()

    output = render_dashboard_json(report)

    assert '"report_id": "dashboard-001"' in output
    assert '"artifact_count": 1' in output


def test_render_dashboard_markdown():
    report = build_report()

    output = render_dashboard_markdown(report)

    assert "# Pipeline Dashboard Report" in output
    assert "dashboard-001" in output
    assert "delivery_report" in output
