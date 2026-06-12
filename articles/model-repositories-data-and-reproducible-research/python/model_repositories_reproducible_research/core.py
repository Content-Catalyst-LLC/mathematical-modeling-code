from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import platform
import sys


@dataclass(frozen=True)
class RepositoryRecord:
    key: str
    repository_layer: str
    artifact: str
    modeling_role: str
    review_question: str
    status: str


@dataclass(frozen=True)
class ExpectedArtifact:
    artifact: str
    path: str
    required: bool
    purpose: str


def parse_bool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "y"}:
        return True
    if normalized in {"false", "0", "no", "n"}:
        return False
    raise ValueError(f"Cannot parse boolean: {value}")


def hash_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return "not_applicable"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(65536), b""):
            digest.update(block)
    return digest.hexdigest()


def artifact_inventory(root: Path, artifacts: list[ExpectedArtifact]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for artifact in artifacts:
        path = root / artifact.path
        exists = path.exists()
        rows.append({
            "artifact": artifact.artifact,
            "path": artifact.path,
            "required": artifact.required,
            "exists": exists,
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "sha256": hash_file(path),
            "purpose": artifact.purpose,
            "review_status": "present" if exists else ("missing_required" if artifact.required else "missing_optional"),
        })
    return rows


def repository_risk_score(record: RepositoryRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.repository_layer} {record.artifact} {record.review_question}".lower()
    for term in ["data", "manifest", "metadata", "governance", "schema", "reproduce", "license", "citation"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def load_records(path: Path) -> list[RepositoryRecord]:
    records: list[RepositoryRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                RepositoryRecord(
                    key=row["key"],
                    repository_layer=row["repository_layer"],
                    artifact=row["artifact"],
                    modeling_role=row["modeling_role"],
                    review_question=row["review_question"],
                    status=row["status"],
                )
            )
    return records


def load_expected_artifacts(path: Path) -> list[ExpectedArtifact]:
    artifacts: list[ExpectedArtifact] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            artifacts.append(
                ExpectedArtifact(
                    artifact=row["artifact"],
                    path=row["path"],
                    required=parse_bool(row["required"]),
                    purpose=row["purpose"],
                )
            )
    return artifacts


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def build_reproducibility_manifest(
    article_root: Path,
    records: list[RepositoryRecord],
    inventory: list[dict[str, object]],
) -> dict[str, object]:
    register_rows = [
        {**asdict(record), "repository_risk_score": repository_risk_score(record)}
        for record in records
    ]
    return {
        "article": "Model Repositories, Data, and Reproducible Research",
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "repository_root": str(article_root),
        "artifact_inventory": inventory,
        "audit_register": register_rows,
        "required_artifacts_missing": [
            row for row in inventory
            if bool(row["required"]) and not bool(row["exists"])
        ],
    }


def build_model_repository_card() -> dict[str, object]:
    return {
        "article": "Model Repositories, Data, and Reproducible Research",
        "model_repository_purpose": "Demonstrate reproducible model repository design.",
        "intended_use": "Educational and analytical workflow governance.",
        "not_for": "Direct operational decisions without domain-specific validation.",
        "data_note": "Synthetic and example data are used for public demonstration.",
        "reuse_note": "Code examples are educational; data and documentation reuse should respect project-specific licenses.",
        "audit_checks": [
            "README and metadata are present",
            "data and documentation folders are present",
            "workflow targets are defined",
            "artifact inventory is generated",
            "reproducibility manifest is written",
        ],
    }
