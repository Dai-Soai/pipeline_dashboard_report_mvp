from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ArtifactSummary:
    artifact_type: str
    source_path: str
    status: str
    total_items: int


@dataclass(frozen=True)
class DashboardReport:
    report_id: str
    generated_at: str
    artifact_count: int
    summary: dict[str, int]
    artifact_types: dict[str, int]
    artifacts: list[ArtifactSummary]


def build_artifact_summary(
    *,
    artifact: dict[str, Any],
    source_path: str,
) -> ArtifactSummary:
    if not isinstance(artifact, dict):
        raise ValueError("artifact must be a JSON object")

    artifact_type = artifact.get("artifact_type")
    if not artifact_type:
        raise ValueError("artifact_type is required")

    summary = artifact.get("summary", {})
    total_items = 0

    if isinstance(summary, dict):
        total_items = int(summary.get("total", 0))

    status = str(artifact.get("status") or artifact.get("result") or "UNKNOWN")

    return ArtifactSummary(
        artifact_type=str(artifact_type),
        source_path=source_path,
        status=status,
        total_items=total_items,
    )


def build_dashboard_status_summary(
    artifacts: list[ArtifactSummary],
) -> dict[str, int]:
    result = {
        "success": 0,
        "failed": 0,
        "warning": 0,
        "unknown": 0,
    }

    for artifact in artifacts:
        status = artifact.status.upper()

        if status in {"SUCCESS", "DELIVERED", "RECORDED"}:
            result["success"] += 1
        elif status in {"FAILED", "ERROR"}:
            result["failed"] += 1
        elif status in {"WARNING", "WARN"}:
            result["warning"] += 1
        else:
            result["unknown"] += 1

    return result


def build_artifact_type_stats(
    artifacts: list[ArtifactSummary],
) -> dict[str, int]:
    result: dict[str, int] = {}

    for artifact in artifacts:
        result[artifact.artifact_type] = result.get(artifact.artifact_type, 0) + 1

    return result


def build_dashboard_report(
    *,
    report_id: str,
    artifacts: list[ArtifactSummary],
) -> DashboardReport:
    return DashboardReport(
        report_id=report_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        artifact_count=len(artifacts),
        summary=build_dashboard_status_summary(artifacts),
        artifact_types=build_artifact_type_stats(artifacts),
        artifacts=artifacts,
    )
