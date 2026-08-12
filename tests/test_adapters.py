import pytest

from testorbit.adapters import KNOWN_RUNNERS, build_task_command


def test_build_task_command_prefers_explicit_command() -> None:
    assert build_task_command({"runner": "npm", "command": "npm run lint"}, "lint") == "npm run lint"


def test_build_task_command_defaults_pytest_runner() -> None:
    assert build_task_command({"runner": "pytest"}, "unit") == "pytest"


def test_build_task_command_defaults_npm_runner() -> None:
    assert build_task_command({"runner": "npm"}, "js") == "npm test"


def test_build_task_command_defaults_jest_runner() -> None:
    assert build_task_command({"runner": "jest"}, "js") == "npx jest"


def test_known_runners_cover_pytest_and_npm() -> None:
    assert KNOWN_RUNNERS["pytest"] == "pytest"
    assert KNOWN_RUNNERS["npm"] == "npm test"


def test_build_task_command_rejects_unknown_runner() -> None:
    with pytest.raises(ValueError, match="must define a command"):
        build_task_command({"runner": "go-test"}, "unit")
