import json

from pipeline_dashboard_report.cli import main


def test_cli_writes_dashboard_reports(tmp_path, monkeypatch):
    input_1 = tmp_path / "delivery_report.json"
    input_2 = tmp_path / "execution_report.json"

    json_output = tmp_path / "dashboard_report.json"
    md_output = tmp_path / "dashboard_report.md"

    input_1.write_text(
        json.dumps(
            {
                "artifact_type": "delivery_report",
                "summary": {"total": 2},
            }
        ),
        encoding="utf-8",
    )

    input_2.write_text(
        json.dumps(
            {
                "artifact_type": "execution_report",
                "status": "SUCCESS",
                "summary": {"total": 3},
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "pipeline-dashboard-report",
            str(input_1),
            str(input_2),
            "--json-output",
            str(json_output),
            "--md-output",
            str(md_output),
        ],
    )

    main()

    json_payload = json.loads(json_output.read_text(encoding="utf-8"))
    md_payload = md_output.read_text(encoding="utf-8")

    assert json_output.exists()
    assert md_output.exists()
    assert json_payload["artifact_count"] == 2
    assert "delivery_report" in md_payload
    assert "execution_report" in md_payload
