from __future__ import annotations

from typing import Any
from uuid import uuid4

from pipeline_dashboard_report.contract import (
    ArtifactSummary,
    DashboardReport,
    build_artifact_summary,
    build_dashboard_report,
)


def build_summaries_from_artifacts(
    artifacts: list[tuple[str, dict[str, Any]]],
) -> list[ArtifactSummary]:
    return [
        build_artifact_summary(
            artifact=artifact,
            source_path=source_path,
        )
        for source_path, artifact in artifacts
    ]


def build_dashboard_from_artifacts(
    artifacts: list[tuple[str, dict[str, Any]]],
) -> DashboardReport:
    summaries = build_summaries_from_artifacts(artifacts)

    return build_dashboard_report(
        report_id=f"dashboard-{uuid4()}",
        artifacts=summaries,
    )
