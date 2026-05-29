from pathlib import Path
from unittest.mock import patch

import pytest
import yaml

from testorbit.cli import load_config, main
from testorbit.history import append_run_result
from testorbit.runner import RunResult


def test_load_config_reads_mapping(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest"}}}), encoding="utf-8")

    data = load_config(config_path)

    assert data["tasks"]["unit"]["command"] == "pytest"


def test_load_config_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        load_config(tmp_path / "missing.yml")


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
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"runner": "pytest"}}}), encoding="utf-8")

    exit_code = main(["doctor", "--config", str(config_path)])

    assert exit_code == 1


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


def test_run_dry_run_reports_command(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}}), encoding="utf-8")

    exit_code = main(["run", "unit", "--dry-run", "--config", str(config_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Would run: pytest tests" in captured.out


def test_run_executes_configured_command(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}}), encoding="utf-8")

    with patch("testorbit.cli.execute_command", return_value=RunResult("unit", "pytest tests", 0, 0.12)) as run_command:
        exit_code = main(["run", "unit", "--config", str(config_path), "--history-path", str(history_path)])

    assert exit_code == 0
    run_command.assert_called_once_with("unit", "pytest tests")
    assert history_path.exists()


def test_run_returns_command_exit_code(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    history_path = tmp_path / "runs.jsonl"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest tests"}}}), encoding="utf-8")

    with patch("testorbit.cli.execute_command", return_value=RunResult("unit", "pytest tests", 2, 0.12)):
        exit_code = main(["run", "unit", "--config", str(config_path), "--history-path", str(history_path)])

    assert exit_code == 2


def test_history_reports_recent_records(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    history_path = tmp_path / "runs.jsonl"
    append_run_result(history_path, RunResult("unit", "pytest tests", 0, 0.42))

    exit_code = main(["history", "--history-path", str(history_path)])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "unit exit=0 duration=0.42s" in captured.out
