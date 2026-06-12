from pathlib import Path
import sys
import tempfile

ARTICLE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ARTICLE_ROOT / "python"))

from model_repositories_reproducible_research.core import (
    ExpectedArtifact,
    RepositoryRecord,
    artifact_inventory,
    hash_file,
    parse_bool,
    repository_risk_score,
)


def test_parse_bool_values():
    assert parse_bool("true") is True
    assert parse_bool("false") is False


def test_artifact_inventory_detects_present_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "README.md").write_text("demo", encoding="utf-8")
        rows = artifact_inventory(root, [ExpectedArtifact("README", "README.md", True, "overview")])
        assert rows[0]["exists"] is True
        assert rows[0]["review_status"] == "present"


def test_hash_file_missing():
    assert hash_file(Path("definitely_missing_file.txt")) == "not_applicable"


def test_repository_risk_score_positive():
    record = RepositoryRecord(
        "run_manifest",
        "reproducibility",
        "reproducibility_manifest.json",
        "Records execution context and output hashes.",
        "Can outputs be regenerated?",
        "active",
    )
    assert repository_risk_score(record) > 0
