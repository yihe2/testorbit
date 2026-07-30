from pathlib import Path

from testorbit.report import CI_HISTORY_PATH, DEFAULT_REPORT_DIR, ci_artifact_paths

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_example_workflow_generates_report_artifacts() -> None:
    text = (REPO_ROOT / "docs/examples/github-actions.yml").read_text(encoding="utf-8")
    history = CI_HISTORY_PATH.as_posix()

    assert f"--history-path {history}" in text
    assert "testorbit --ci report" in text
    assert "testorbit --ci export-history" in text
    assert "path: reports/" in text


def test_repo_workflow_renders_report_after_tests() -> None:
    text = (REPO_ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "pytest" in text
    assert "testorbit --ci report" in text
    assert CI_HISTORY_PATH.as_posix() in text
    assert "path: reports/" in text


def test_ci_artifact_paths_share_reports_directory() -> None:
    paths = ci_artifact_paths()

    assert paths["history"] == CI_HISTORY_PATH
    assert {path.parent for path in paths.values()} == {DEFAULT_REPORT_DIR}
