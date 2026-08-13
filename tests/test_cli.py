from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from testorbit.cli import main
from testorbit.history import append_run_result
from testorbit.runner import RunResult


def test_doctor_reports_discovered_tasks(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"unit": {"command": "pytest"}, "smoke": {"command": "pytest -m smoke"}}}),
        encoding="utf-8",
    )

    exit_code = main(["doctor", "--config", str(config_path)])

    assert exit_code == 0


def test_doctor_rejects_task_without_command(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"tags": ["fast"]}}}), encoding="utf-8")

    exit_code = main(["doctor", "--config", str(config_path)])

    assert exit_code == 1


def test_init_creates_config_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "project" / "testorbit.yml"

    exit_code = main(["init", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert config_path.exists()
    assert f"Created {config_path} with 3 task(s)." in captured.out
    assert "testorbit doctor" in captured.out
    assert "testorbit list" in captured.out
    assert "testorbit run unit --dry-run" in captured.out


def test_init_rejects_existing_config(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text("tasks: {}\n", encoding="utf-8")

    assert main(["init", "--config", str(config_path)]) == 1


def test_init_force_overwrites_existing_config(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text("tasks: {}\n", encoding="utf-8")

    exit_code = main(["init", "--config", str(config_path), "--force"])

    assert exit_code == 0
    assert "unit" in yaml.safe_load(config_path.read_text(encoding="utf-8"))["tasks"]


def test_list_reports_task_names(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"unit": {"command": "pytest"}, "smoke": {"command": "pytest -m smoke"}}}),
        encoding="utf-8",
    )

    exit_code = main(["list", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Configured tasks:" in captured.out
    assert "- smoke" in captured.out
    assert "- unit" in captured.out


def test_show_reports_task_details(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests", "runner": "pytest"}}}),
        encoding="utf-8",
    )

    exit_code = main(["show", "unit", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Task: unit" in captured.out
    assert "command: pytest tests" in captured.out
    assert "runner: pytest" in captured.out


def test_list_marks_quarantined_tasks(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "tasks": {"unit": {"command": "pytest"}, "smoke": {"command": "pytest -m smoke"}},
                "quarantine": ["smoke"],
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(["list", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "- smoke [quarantined]" in captured.out
    assert "- unit" in captured.out
    assert "- unit [quarantined]" not in captured.out


def test_show_marks_quarantined_task(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"smoke": {"command": "pytest -m smoke"}}, "quarantine": ["smoke"]}),
        encoding="utf-8",
    )

    exit_code = main(["show", "smoke", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Task: smoke" in captured.out
    assert "Status: quarantined" in captured.out


def test_list_includes_last_run_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"unit": {"command": "pytest"}, "smoke": {"command": "pytest -m smoke"}}}),
        encoding="utf-8",
    )
    append_run_result(history_path, RunResult("unit", "pytest", 0, 0.42))
    append_run_result(history_path, RunResult("unit", "pytest", 1, 0.8))

    exit_code = main(["list", "--config", str(config_path), "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "- unit last=failed (0.8s)" in captured.out
    assert "- smoke last=none" in captured.out


def test_show_includes_last_run_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}}),
        encoding="utf-8",
    )
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))

    exit_code = main(["show", "unit", "--config", str(config_path), "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Last run: passed (0.42s)" in captured.out


def test_list_reports_empty_config(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(yaml.safe_dump({"tasks": {}}), encoding="utf-8")

    exit_code = main(["list", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "No tasks configured." in captured.out


def test_list_help_mentions_last_run_status(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["list", "--help"])

    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert "last run status" in captured.out


def test_root_help_mentions_ci_mode(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    captured = capsys.readouterr()
    assert exc_info.value.code == 0
    assert "--ci" in captured.out
    assert "CI logs" in captured.out


def test_ci_mode_prints_plain_doctor_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest"}}}), encoding="utf-8")

    exit_code = main(["--ci", "doctor", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Discovered 1 task(s)" in captured.out
    assert "\x1b[" not in captured.out
    assert "\x1b[" not in captured.err


def test_ci_mode_omits_report_open_link(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    history_path = tmp_path / "runs.jsonl"
    output_path = tmp_path / "summary.html"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))

    exit_code = main(
        ["--ci", "report", "--history-path", str(history_path), "--output", str(output_path)]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert f"Wrote report to {output_path.resolve()}" in captured.out
    assert "Open " not in captured.out
    assert "file://" not in captured.out


def test_ci_mode_skips_init_next_steps(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"

    exit_code = main(["--ci", "init", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert f"Created {config_path} with 3 task(s)." in captured.out
    assert "Next:" not in captured.out


def test_run_dry_run_reports_command(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}}), encoding="utf-8")

    exit_code = main(["run", "unit", "--dry-run", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Would run: pytest tests" in captured.out


def test_run_executes_configured_command(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}}), encoding="utf-8")

    with patch("testorbit.cli.execute_command", return_value=RunResult("unit", "pytest tests", 0, 0.12)) as run_command:
        exit_code = main(["run", "unit", "--config", str(config_path), "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    run_command.assert_called_once_with("unit", "pytest tests")
    assert history_path.exists()
    assert "Task 'unit' passed" in captured.out
    assert "Finished in 0.12s" in captured.out


def test_run_returns_command_exit_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}}), encoding="utf-8")

    with patch("testorbit.cli.execute_command", return_value=RunResult("unit", "pytest tests", 2, 0.12)):
        exit_code = main(["run", "unit", "--config", str(config_path), "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 2
    assert "failed with exit 2" in captured.out


def test_run_reports_missing_tool(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "missing-tool tests"}}}), encoding="utf-8")

    with patch("testorbit.runner.shutil.which", return_value=None):
        exit_code = main(["run", "unit", "--config", str(config_path), "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Command not found: missing-tool" in captured.out
    assert not history_path.exists()


def test_run_reports_permission_denied(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}}), encoding="utf-8")

    with (
        patch("testorbit.runner.shutil.which", return_value="pytest"),
        patch("testorbit.runner.subprocess.run", side_effect=PermissionError("pytest")),
    ):
        exit_code = main(["run", "unit", "--config", str(config_path), "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Permission denied: pytest" in captured.out
    assert not history_path.exists()


def test_run_skips_quarantined_task(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}, "quarantine": ["unit"]}),
        encoding="utf-8",
    )

    with patch("testorbit.cli.execute_command") as run_command:
        exit_code = main(["run", "unit", "--config", str(config_path), "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    run_command.assert_not_called()
    assert not history_path.exists()
    assert "Skipping quarantined task 'unit'" in captured.out


def test_run_skips_quarantined_task_on_dry_run(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}, "quarantine": ["unit"]}),
        encoding="utf-8",
    )

    exit_code = main(["run", "unit", "--dry-run", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Skipping quarantined task 'unit'" in captured.out
    assert "Would run:" not in captured.out


def test_run_rejects_unknown_quarantined_task(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(
        yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}, "quarantine": ["smoke"]}),
        encoding="utf-8",
    )

    assert main(["run", "unit", "--config", str(config_path)]) == 1


def test_doctor_warns_when_quarantine_is_active(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "tasks": {"unit": {"command": "pytest"}, "smoke": {"command": "pytest -m smoke"}},
                "quarantine": ["smoke"],
            }
        ),
        encoding="utf-8",
    )

    exit_code = main(["doctor", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Discovered 2 task(s)" in captured.out
    assert "Quarantine active: smoke" in captured.out


def test_history_reports_recent_records(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    history_path = tmp_path / "runs.jsonl"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))

    exit_code = main(["history", "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Runs: 1 total, 1 passed, 0 failed" in captured.out
    assert "unit exit=0 duration=0.42s" in captured.out
    assert "Flaky:" not in captured.out


def test_history_reports_flaky_task_names(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    history_path = tmp_path / "runs.jsonl"
    append_run_result(history_path, RunResult("unit", "pytest tests", 1, 0.4))
    append_run_result(history_path, RunResult("unit", "pytest tests", 1, 0.5))

    exit_code = main(["history", "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Flaky: unit" in captured.out


def test_history_filters_records_by_status(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    history_path = tmp_path / "runs.jsonl"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))
    append_run_result(history_path, RunResult("smoke", "pytest -m smoke", 1, 0.7))

    exit_code = main(["history", "--history-path", str(history_path), "--status", "failed"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "smoke exit=1 duration=0.7s" in captured.out
    assert "unit exit=0" not in captured.out


def test_history_rejects_invalid_limit(tmp_path: Path) -> None:
    exit_code = main(["history", "--history-path", str(tmp_path / "runs.jsonl"), "--limit", "0"])

    assert exit_code == 1


def test_export_history_writes_json_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    history_path = tmp_path / "runs.jsonl"
    export_path = tmp_path / "exports" / "runs.json"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))

    exit_code = main(["export-history", "--history-path", str(history_path), "--output", str(export_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Exported 1 record(s)" in captured.out
    assert export_path.exists()


def test_report_writes_html_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    history_path = tmp_path / "runs.jsonl"
    output_path = tmp_path / "reports" / "summary.html"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))

    exit_code = main(
        ["report", "--history-path", str(history_path), "--output", str(output_path)]
    )
    captured = capsys.readouterr()
    html = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert f"Wrote report to {output_path.resolve()}" in captured.out
    assert output_path.resolve().as_uri() in captured.out
    assert "1 passed, 0 failed across 1 runs" in html
    assert "unit" in html


def test_report_filters_records_by_status(tmp_path: Path) -> None:
    history_path = tmp_path / "runs.jsonl"
    output_path = tmp_path / "summary.html"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))
    append_run_result(history_path, RunResult("smoke", "pytest -m smoke", 1, 0.7))

    exit_code = main(
        ["report", "--history-path", str(history_path), "--output", str(output_path), "--status", "failed"]
    )
    html = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert "0 passed, 1 failed across 1 runs" in html
    assert "smoke" in html
    assert "unit" not in html


def test_report_end_to_end_from_history_file(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    history_path = tmp_path / "run-history" / "runs.jsonl"
    output_path = tmp_path / "reports" / "summary.html"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))
    append_run_result(history_path, RunResult("api", "pytest tests/api", 1, 1.5))

    exit_code = main(["report", "--history-path", str(history_path), "--output", str(output_path)])
    captured = capsys.readouterr()
    html = output_path.read_text(encoding="utf-8")

    assert exit_code == 0
    assert output_path.exists()
    assert f"Wrote report to {output_path.resolve()}" in captured.out
    assert output_path.resolve().as_uri() in captured.out
    assert "1 passed, 1 failed across 2 runs" in html
    assert 'class="card total"' in html
    assert "width: 50.0%" in html
    assert "<td>unit</td>" in html
    assert "<td>api</td>" in html
    assert 'tr class="passed"' in html or 'class="passed"' in html
    assert 'class="failed"' in html
