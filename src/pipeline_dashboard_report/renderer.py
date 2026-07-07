from __future__ import annotations

import json
from dataclasses import asdict

from pipeline_dashboard_report.contract import DashboardReport


def render_dashboard_json(report: DashboardReport) -> str:
    return json.dumps(
        asdict(report),
        indent=2,
        ensure_ascii=False,
    )


def render_dashboard_markdown(report: DashboardReport) -> str:
    lines = [
        "# Pipeline Dashboard Report",
        "",
        f"Report ID: {report.report_id}",
        f"Generated: {report.generated_at}",
        "",
        f"Artifacts: **{report.artifact_count}**",
        "",
        "## Summary",
        "",
        f"- Success: {report.summary['success']}",
        f"- Failed: {report.summary['failed']}",
        f"- Warning: {report.summary['warning']}",
        f"- Unknown: {report.summary['unknown']}",
        "",
        "## Artifact Types",
        "",
    ]

    for artifact_type, count in report.artifact_types.items():
        lines.append(f"- {artifact_type}: {count}")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "| Artifact | Status | Items | Source |",
            "|----------|--------|-------|--------|",
        ]
    )

    for artifact in report.artifacts:
        lines.append(
            f"| {artifact.artifact_type} "
            f"| {artifact.status} "
            f"| {artifact.total_items} "
            f"| {artifact.source_path} |"
        )

    return "\n".join(lines)
