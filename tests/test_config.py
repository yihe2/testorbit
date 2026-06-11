from pathlib import Path

import pytest
import yaml

from testorbit.config import get_tasks, load_config, validate_tasks


def test_load_config_reads_mapping(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text(yaml.safe_dump({"tasks": {"unit": {"command": "pytest"}}}), encoding="utf-8")

    data = load_config(config_path)

    assert data["tasks"]["unit"]["command"] == "pytest"


def test_load_config_rejects_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Config file not found"):
        load_config(tmp_path / "missing.yml")


def test_load_config_rejects_non_mapping(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text("- unit\n", encoding="utf-8")

    with pytest.raises(ValueError, match="mapping at the top level"):
        load_config(config_path)


def test_get_tasks_requires_mapping() -> None:
    with pytest.raises(ValueError, match="'tasks' must be a mapping"):
        get_tasks({"tasks": ["unit"]})


def test_validate_tasks_requires_command() -> None:
    with pytest.raises(ValueError, match="must define a command"):
        validate_tasks({"unit": {"runner": "pytest"}})
