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
    assert summary.records == tuple(records)


def test_report_summary_serializes_for_templates() -> None:
    records = [{"task_name": "unit", "status": "passed", "exit_code": 0}]

    assert ReportSummary.from_records(records).to_dict() == {
        "total": 1,
        "passed": 1,
        "failed": 0,
        "records": records,
    }


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
    assert "unit" in text
    assert "smoke" in text
    assert "failed" in text


def test_render_html_report_handles_empty_history(tmp_path: Path) -> None:
    output_path = tmp_path / "nested" / "summary.html"
    text = render_html_report(ReportSummary.from_records([]), output_path).read_text(encoding="utf-8")

    assert output_path.exists()
    assert "0 passed, 0 failed, 0 total" in text
    assert "No run history found." in text


def test_build_report_reads_history_file(tmp_path: Path) -> None:
    history_path = tmp_path / "runs.jsonl"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))
    append_run_result(history_path, RunResult("smoke", "pytest -m smoke", 1, 0.7))

    summary = build_report(history_path, status="failed")

    assert summary.total == 1
    assert summary.failed == 1
    assert summary.records[0]["task_name"] == "smoke"
