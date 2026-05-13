from pathlib import Path

import pytest
import yaml

from testorbit.cli import load_config, main


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
