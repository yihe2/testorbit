from pathlib import Path

from testorbit.history import append_run_result
from testorbit.report import (
    DEFAULT_EXPORT_PATH,
    DEFAULT_REPORT_DIR,
    DEFAULT_REPORT_PATH,
    SUMMARY_TEMPLATE,
    TEMPLATES_DIR,
    ReportSummary,
    build_report,
    render_html_report,
)
from testorbit.runner import RunResult


def test_report_summary_from_records() -> None:
    records = [
        {"task_name": "unit", "status": "passed", "exit_code": 0, "duration_seconds": 0.42},
        {"task_name": "smoke", "status": "failed", "exit_code": 1, "duration_seconds": 0.8},
    ]

    summary = ReportSummary.from_records(records)

    assert summary.total == 2
    assert summary.passed == 1
    assert summary.failed == 1
    assert summary.records[0]["task_name"] == "unit"
    assert summary.records[0]["duration_display"] == "0.42s"
    assert summary.records[1]["duration_display"] == "0.8s"
    assert summary.flaky_tasks == ()


def test_report_summary_serializes_for_templates() -> None:
    records = [{"task_name": "unit", "status": "passed", "exit_code": 0}]
    payload = ReportSummary.from_records(records).to_dict()

    assert payload["total"] == 1
    assert payload["passed"] == 1
    assert payload["failed"] == 0
    assert payload["pass_percent"] == 100.0
    assert payload["fail_percent"] == 0.0
    assert payload["flaky_tasks"] == []
    assert payload["flaky_count"] == 0
    assert payload["records"][0]["duration_display"] == "—"


def test_report_summary_includes_flaky_tasks() -> None:
    records = [
        {"task_name": "unit", "status": "failed", "exit_code": 1},
        {"task_name": "unit", "status": "failed", "exit_code": 1},
    ]

    assert ReportSummary.from_records(records).flaky_tasks == ("unit",)


def test_artifact_paths_live_under_reports_dir() -> None:
    assert DEFAULT_REPORT_PATH.parent == DEFAULT_REPORT_DIR
    assert DEFAULT_EXPORT_PATH.parent == DEFAULT_REPORT_DIR
    assert DEFAULT_REPORT_PATH.name == "summary.html"
    assert DEFAULT_EXPORT_PATH.name == "runs.json"


def test_summary_template_scaffold_exists() -> None:
    template_path = TEMPLATES_DIR / SUMMARY_TEMPLATE
    text = template_path.read_text(encoding="utf-8")

    assert template_path.exists()
    assert "TestOrbit Summary" in text
    assert "{{ passed }}" in text
    assert 'class="cards"' in text
    assert 'class="card passed"' in text
    assert 'class="card flaky"' in text
    assert 'class="chart"' in text
    assert "--passed:" in text
    assert "flaky-hint" in text
    assert "{% for record in records %}" in text


def test_render_html_report_writes_summary(tmp_path: Path) -> None:
    output_path = tmp_path / "summary.html"
    records = [
        {"task_name": "unit", "status": "passed", "exit_code": 0, "duration_seconds": 0.42},
        {"task_name": "smoke", "status": "failed", "exit_code": 1, "duration_seconds": 0.8},
    ]

    written = render_html_report(ReportSummary.from_records(records), output_path)
    text = written.read_text(encoding="utf-8")

    assert written == output_path
    assert "1 passed, 1 failed, 2 total" in text
    assert 'class="card passed"' in text
    assert "width: 50.0%" in text
    assert "unit" in text
    assert "smoke" in text
    assert "failed" in text


def test_render_html_report_handles_empty_history(tmp_path: Path) -> None:
    output_path = tmp_path / "nested" / "summary.html"
    text = render_html_report(ReportSummary.from_records([]), output_path).read_text(encoding="utf-8")

    assert output_path.exists()
    assert "0 passed, 0 failed, 0 total" in text
    assert "No run history found." in text
    assert "Flaky tasks" not in text


def test_render_html_report_surfaces_flaky_hint(tmp_path: Path) -> None:
    html = render_html_report(
        ReportSummary.from_records(
            [
                {"task_name": "unit", "status": "failed", "exit_code": 1, "duration_seconds": 0.4},
                {"task_name": "unit", "status": "failed", "exit_code": 1, "duration_seconds": 0.5},
            ]
        ),
        tmp_path / "summary.html",
    ).read_text(encoding="utf-8")

    assert "Flaky tasks (2+ failures): unit" in html
    assert "flaky" in html


def test_report_normalizes_missing_fields(tmp_path: Path) -> None:
    html = render_html_report(
        ReportSummary.from_records([{"exit_code": 1}]),
        tmp_path / "summary.html",
    ).read_text(encoding="utf-8")

    assert "(unknown)" in html
    assert "failed" in html
    assert "—" in html


def test_report_escapes_task_names(tmp_path: Path) -> None:
    html = render_html_report(
        ReportSummary.from_records(
            [{"task_name": "<script>alert(1)</script>", "status": "passed", "exit_code": 0, "duration_seconds": 0.1}]
        ),
        tmp_path / "summary.html",
    ).read_text(encoding="utf-8")

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_build_report_reads_history_file(tmp_path: Path) -> None:
    history_path = tmp_path / "runs.jsonl"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))
    append_run_result(history_path, RunResult("smoke", "pytest -m smoke", 1, 0.7))

    summary = build_report(history_path, status="failed")

    assert summary.total == 1
    assert summary.failed == 1
    assert summary.records[0]["task_name"] == "smoke"
