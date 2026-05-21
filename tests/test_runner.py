from unittest.mock import Mock, patch

import pytest

from testorbit.runner import execute_command


def test_execute_command_returns_run_result() -> None:
    with (
        patch("testorbit.runner.subprocess.run", return_value=Mock(returncode=0)) as run_command,
        patch("testorbit.runner.time.perf_counter", side_effect=[12.0, 12.34]),
    ):
        result = execute_command("unit", "pytest tests")

    assert result.task_name == "unit"
    assert result.command == "pytest tests"
    assert result.exit_code == 0
    assert result.duration_seconds == pytest.approx(0.34)
    run_command.assert_called_once_with("pytest tests", shell=True, check=False)
