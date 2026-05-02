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
