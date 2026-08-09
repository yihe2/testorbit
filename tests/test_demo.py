from pathlib import Path

import pytest

from testorbit.cli import main
from testorbit.config import get_tasks, load_config, resolve_quarantine, validate_tasks

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_ROOT = REPO_ROOT / "examples" / "demo"
DEMO_CONFIG = DEMO_ROOT / "testorbit.yml"


def test_demo_config_is_valid() -> None:
    data = load_config(DEMO_CONFIG)
    tasks = get_tasks(data)
    validate_tasks(tasks)
    resolve_quarantine(data, tasks)

    assert set(tasks) == {"unit", "smoke", "api"}
    assert tasks["unit"]["command"] == "pytest tests"
    assert tasks["smoke"]["command"] == "pytest -m smoke"
    assert tasks["api"]["command"] == "pytest tests/api"


def test_demo_doctor_lists_three_tasks(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["doctor", "--config", str(DEMO_CONFIG)]) == 0
    captured = capsys.readouterr()

    assert "Discovered 3 task(s)" in captured.out


def test_demo_list_and_dry_run_match_quickstart(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["list", "--config", str(DEMO_CONFIG)]) == 0
    listed = capsys.readouterr().out
    assert "- api" in listed
    assert "- smoke" in listed
    assert "- unit" in listed

    assert main(["run", "unit", "--dry-run", "--config", str(DEMO_CONFIG)]) == 0
    assert "Would run: pytest tests" in capsys.readouterr().out


def test_quickstart_documents_demo_flow() -> None:
    text = (REPO_ROOT / "docs" / "quickstart.md").read_text(encoding="utf-8")

    assert "cd examples/demo" in text
    assert "testorbit doctor" in text
    assert "testorbit list" in text
    assert "testorbit run unit --dry-run" in text


def test_setup_notes_cover_install_and_demo() -> None:
    text = (REPO_ROOT / "docs" / "setup.md").read_text(encoding="utf-8")

    assert 'pip install -e ".[dev]"' in text
    assert "examples/demo" in text
    assert "testorbit version" in text


def test_demo_sample_tests_exist() -> None:
    assert (DEMO_ROOT / "shop.py").exists()
    assert (DEMO_ROOT / "tests" / "test_shop.py").exists()
    assert (DEMO_ROOT / "tests" / "test_smoke.py").exists()
    assert (DEMO_ROOT / "tests" / "api" / "test_orders.py").exists()
