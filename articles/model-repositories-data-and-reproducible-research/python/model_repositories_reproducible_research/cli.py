from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from model_repositories_reproducible_research.core import (
    artifact_inventory,
    build_model_repository_card,
    build_reproducibility_manifest,
    load_expected_artifacts,
    load_records,
    repository_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run model repository reproducibility audit.")
    parser.add_argument("--register-file", type=Path, default=Path("data/repository_audit_register.csv"))
    parser.add_argument("--expected-artifacts-file", type=Path, default=Path("data/expected_repository_artifacts.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    article_root = Path.cwd()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_records(args.register_file)
    expected = load_expected_artifacts(args.expected_artifacts_file)
    inventory = artifact_inventory(article_root, expected)

    register_rows = [
        {**asdict(record), "repository_risk_score": repository_risk_score(record)}
        for record in records
    ]

    inventory_path = tables_dir / "repository_artifact_inventory.csv"
    register_path = tables_dir / "repository_audit_register.csv"
    manifest_path = json_dir / "reproducibility_manifest.json"
    model_card_path = json_dir / "model_repository_card.json"

    write_csv(inventory_path, inventory)
    write_csv(register_path, register_rows)
    write_json(manifest_path, build_reproducibility_manifest(article_root, records, inventory))
    write_json(model_card_path, build_model_repository_card())

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "repository_audit.log").write_text(
        "Repository reproducibility audit completed successfully.\n",
        encoding="utf-8",
    )

    print("Repository reproducibility audit complete.")
    print(f"Repository records: {len(records)}")
    print(f"Expected artifacts: {len(expected)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
