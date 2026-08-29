from testorbit import __version__
from testorbit.cli import main
import pytest


def test_package_version_is_1_0_0() -> None:
    assert __version__ == "1.0.0"


def test_version_command_prints_package_version(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["version"]) == 0
    captured = capsys.readouterr()
    assert f"TestOrbit {__version__}" in captured.out
