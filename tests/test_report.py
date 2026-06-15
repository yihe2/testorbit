from testorbit.report import ReportSummary


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


def test_report_summary_handles_empty_history() -> None:
    summary = ReportSummary.from_records([])

    assert summary.to_dict() == {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "records": [],
    }
