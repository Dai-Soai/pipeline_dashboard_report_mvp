# Pipeline Dashboard Report MVP

RADAR Service Utility #23

Version: v0.1.0

## Overview

Pipeline Dashboard Report reads RADAR_SERVICE pipeline artifacts and generates dashboard reports in JSON and Markdown formats.

It provides a lightweight summary layer for pipeline status, artifact counts, status distribution, and artifact type statistics.

## Artifact Flow

```text
pipeline artifacts
        │
        ▼
read_json_artifact()
        │
        ▼
build_dashboard_from_artifacts()
        │
        ▼
render_dashboard_json()
        │
        ├── dashboard_report.json
        │
        ▼
render_dashboard_markdown()
        └── dashboard_report.md
 ```

## Input Artifacts

Supported inputs include:

- monitor_report.json
- retry_plan.json
- schedule.json
- execution_report.json
- notification_report.json
- delivery_report.json

## Output Artifacts

reports/dashboard_report.json
reports/dashboard_report.md

## Module Responsibilities

contract.py

Defines dashboard data structures and summary contracts.

reader.py

Reads and validates pipeline artifact JSON and JSONL files.

summary.py

Builds dashboard reports from loaded artifacts.

renderer.py

Renders dashboard reports into JSON and Markdown.

cli.py

Provides command-line execution.

## Project Structure

src/pipeline_dashboard_report/
    contract.py
    reader.py
    summary.py
    renderer.py
    cli.py

tests/
samples/
reports/

## Installation

python -m venv .venv
source .venv/bin/activate

pip install -e .

## CLI Usage

pipeline-dashboard-report \
    samples/delivery_report.json \
    samples/execution_report.json

Custom output:

pipeline-dashboard-report \
    samples/delivery_report.json \
    samples/execution_report.json \
    --json-output reports/dashboard_report.json \
    --md-output reports/dashboard_report.md

## Dashboard JSON Includes

- report_id
- generated_at
- artifact_count
- summary
    - success
    - failed
    - warning
    - unknown
- artifact_types
- artifacts

## Dashboard Markdown Includes

- Pipeline dashboard title
- Report ID
- Generated timestamp
- Status summary
- Artifact type statistics
- Artifact table

## Testing

pytest

Current status:

19 passed

## Responsibility

- Read pipeline artifact files
- Validate artifact input
- Build dashboard summary
- Render JSON dashboard report
- Render Markdown dashboard report
- Provide CLI execution

## Not Responsibility

- Web dashboard
- Runtime integration
- Database storage
- Notification sending
- Real-time monitoring
- Chart rendering
