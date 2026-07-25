from pathlib import Path

import pytest
import yaml

from testorbit.config import (
    QUARANTINE_KEY,
    get_quarantine,
    get_tasks,
    is_quarantined,
    load_config,
    resolve_quarantine,
    starter_config,
    validate_quarantine,
    validate_tasks,
    write_starter_config,
)


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


def test_starter_config_includes_pytest_presets() -> None:
    tasks = get_tasks(starter_config())

    assert set(tasks) == {"unit", "smoke", "api"}
    validate_tasks(tasks)
    assert tasks["unit"]["command"] == "pytest tests"


def test_write_starter_config_creates_valid_file(tmp_path: Path) -> None:
    config_path = tmp_path / "nested" / "testorbit.yml"
    write_starter_config(config_path)

    data = load_config(config_path)
    validate_tasks(get_tasks(data))
    assert config_path.exists()


def test_write_starter_config_rejects_existing_file(tmp_path: Path) -> None:
    config_path = tmp_path / "testorbit.yml"
    config_path.write_text("tasks: {}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="already exists"):
        write_starter_config(config_path)


def test_get_quarantine_defaults_to_empty_list() -> None:
    assert get_quarantine({"tasks": {"unit": {"command": "pytest"}}}) == []


def test_get_quarantine_reads_task_names() -> None:
    data = {"tasks": {"smoke": {"command": "pytest -m smoke"}}, "quarantine": ["smoke"]}

    assert get_quarantine(data) == ["smoke"]


def test_get_quarantine_rejects_non_list() -> None:
    with pytest.raises(ValueError, match="'quarantine' must be a list"):
        get_quarantine({"quarantine": "smoke"})


def test_validate_quarantine_rejects_unknown_task() -> None:
    with pytest.raises(ValueError, match="Unknown quarantined task"):
        validate_quarantine({"unit": {"command": "pytest"}}, ["smoke"])


def test_resolve_quarantine_returns_validated_names() -> None:
    data = {"tasks": {"smoke": {"command": "pytest -m smoke"}}, QUARANTINE_KEY: ["smoke"]}
    tasks = get_tasks(data)

    assert resolve_quarantine(data, tasks) == ["smoke"]


def test_is_quarantined_matches_listed_names() -> None:
    assert is_quarantined("smoke", ["smoke"])
    assert not is_quarantined("unit", ["smoke"])
