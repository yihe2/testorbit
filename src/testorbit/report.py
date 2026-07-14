from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from testorbit.history import filter_run_history, flaky_task_names, read_run_history, summarize_run_history

TEMPLATES_DIR = Path(__file__).parent / "templates"
SUMMARY_TEMPLATE = "summary.html.j2"
DEFAULT_REPORT_DIR = Path("reports")
DEFAULT_REPORT_PATH = DEFAULT_REPORT_DIR / "summary.html"
DEFAULT_EXPORT_PATH = DEFAULT_REPORT_DIR / "runs.json"


def _normalize_record(record: dict) -> dict:
    exit_code = record.get("exit_code", 1)
    status = record.get("status")
    if status not in {"passed", "failed"}:
        status = "passed" if exit_code == 0 else "failed"

    duration = record.get("duration_seconds")
    duration_display = "—" if duration is None else f"{duration}s"

    return {
        **record,
        "task_name": record.get("task_name") or "(unknown)",
        "status": status,
        "duration_display": duration_display,
    }


@dataclass(frozen=True)
class ReportSummary:
    total: int
    passed: int
    failed: int
    records: tuple[dict, ...]
    flaky_tasks: tuple[str, ...]

    @classmethod
    def from_records(cls, records: list[dict]) -> ReportSummary:
        normalized = [_normalize_record(record) for record in records]
        summary = summarize_run_history(normalized)
        return cls(
            total=summary["total"],
            passed=summary["passed"],
            failed=summary["failed"],
            records=tuple(normalized),
            flaky_tasks=tuple(flaky_task_names(normalized)),
        )

    @property
    def pass_percent(self) -> float:
        if self.total == 0:
            return 0.0
        return round(100 * self.passed / self.total, 1)

    @property
    def fail_percent(self) -> float:
        if self.total == 0:
            return 0.0
        return round(100 - self.pass_percent, 1)

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "pass_percent": self.pass_percent,
            "fail_percent": self.fail_percent,
            "flaky_tasks": list(self.flaky_tasks),
            "flaky_count": len(self.flaky_tasks),
            "records": list(self.records),
        }


def _template_environment() -> Environment:
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "j2"]),
    )


def build_report(history_path: Path, status: str | None = None) -> ReportSummary:
    records = filter_run_history(read_run_history(history_path), status)
    return ReportSummary.from_records(records)


def render_html_report(summary: ReportSummary, output_path: Path) -> Path:
    html = _template_environment().get_template(SUMMARY_TEMPLATE).render(**summary.to_dict())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
