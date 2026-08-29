import tomllib
from pathlib import Path

from testorbit import __version__
from testorbit.cli import main
from testorbit.report import SUMMARY_TEMPLATE, TEMPLATES_DIR

REPO_ROOT = Path(__file__).resolve().parents[1]
DEMO_CONFIG = REPO_ROOT / "examples" / "demo" / "testorbit.yml"


def test_pyproject_version_matches_package() -> None:
    data = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert data["project"]["version"] == __version__ == "1.0.0"


def test_changelog_documents_1_0_0() -> None:
    text = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert "## 1.0.0" in text
    assert "2026-08-31" in text


def test_release_checklist_covers_version_and_tests() -> None:
    text = (REPO_ROOT / "docs" / "release-checklist.md").read_text(encoding="utf-8")

    assert "testorbit version" in text
    assert "pytest" in text
    assert "examples/demo" in text


def test_setup_notes_expect_released_version() -> None:
    text = (REPO_ROOT / "docs" / "setup.md").read_text(encoding="utf-8")

    assert f"TestOrbit {__version__}" in text


def test_html_template_is_packaged() -> None:
    assert (TEMPLATES_DIR / SUMMARY_TEMPLATE).is_file()


def test_demo_dry_run_still_works() -> None:
    assert main(["run", "unit", "--dry-run", "--config", str(DEMO_CONFIG)]) == 0
