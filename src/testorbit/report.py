from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from testorbit.history import summarize_run_history

TEMPLATES_DIR = Path(__file__).parent / "templates"
SUMMARY_TEMPLATE = "summary.html.j2"


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
