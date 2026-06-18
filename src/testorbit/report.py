from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from testorbit.history import summarize_run_history

TEMPLATES_DIR = Path(__file__).parent / "templates"
SUMMARY_TEMPLATE = "summary.html.j2"
DEFAULT_REPORT_DIR = Path("reports")
DEFAULT_REPORT_PATH = DEFAULT_REPORT_DIR / "summary.html"
DEFAULT_EXPORT_PATH = DEFAULT_REPORT_DIR / "runs.json"


@dataclass(frozen=True)
class ReportSummary:
    total: int
    passed: int
    failed: int
    records: tuple[dict, ...]

    @classmethod
    def from_records(cls, records: list[dict]) -> ReportSummary:
        summary = summarize_run_history(records)
        return cls(
            total=summary["total"],
            passed=summary["passed"],
            failed=summary["failed"],
            records=tuple(records),
        )

    def to_dict(self) -> dict:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "records": list(self.records),
        }


def render_html_report(summary: ReportSummary, output_path: Path) -> Path:
    environment = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html", "j2"]),
    )
    html = environment.get_template(SUMMARY_TEMPLATE).render(**summary.to_dict())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    return output_path
