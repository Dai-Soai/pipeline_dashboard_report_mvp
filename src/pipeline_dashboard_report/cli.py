from __future__ import annotations

import argparse
from pathlib import Path

from pipeline_dashboard_report.reader import read_json_artifact
from pipeline_dashboard_report.renderer import (
    render_dashboard_json,
    render_dashboard_markdown,
)
from pipeline_dashboard_report.summary import build_dashboard_from_artifacts


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline Dashboard Report MVP")

    parser.add_argument(
        "inputs",
        nargs="+",
        help="Path(s) to pipeline artifact JSON files",
    )

    parser.add_argument(
        "--json-output",
        default="reports/dashboard_report.json",
        help="Path to dashboard JSON report",
    )

    parser.add_argument(
        "--md-output",
        default="reports/dashboard_report.md",
        help="Path to dashboard Markdown report",
    )

    args = parser.parse_args()

    artifacts = []

    for input_path in args.inputs:
        path = Path(input_path)
        artifact = read_json_artifact(path)
        artifacts.append((str(path), artifact))

    report = build_dashboard_from_artifacts(artifacts)

    json_output = Path(args.json_output)
    md_output = Path(args.md_output)

    json_output.parent.mkdir(parents=True, exist_ok=True)
    md_output.parent.mkdir(parents=True, exist_ok=True)

    json_output.write_text(
        render_dashboard_json(report) + "\n",
        encoding="utf-8",
    )

    md_output.write_text(
        render_dashboard_markdown(report) + "\n",
        encoding="utf-8",
    )

    print(f"Dashboard JSON written to {json_output}")
    print(f"Dashboard Markdown written to {md_output}")


if __name__ == "__main__":
    main()
