from pathlib import Path
import sys

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from reproducible_calculus_workflows.cli import build_artifacts, build_run_record

def test_artifact_count():
    assert len(build_artifacts()) >= 4

def test_artifact_has_source_and_generated():
    origins = {artifact.source_or_generated for artifact in build_artifacts()}
    assert "source" in origins
    assert "generated" in origins

def test_run_record_expected_outputs():
    artifacts = build_artifacts()
    record = build_run_record(artifacts)
    assert record.expected_outputs == len(artifacts)

def test_run_record_command():
    assert build_run_record(build_artifacts()).command == "make smoke"
