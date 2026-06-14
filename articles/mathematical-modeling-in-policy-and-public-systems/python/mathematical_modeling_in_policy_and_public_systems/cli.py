from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from mathematical_modeling_in_policy_and_public_systems.core import (
    build_policy_decision_support_card,
    evaluate_policy_option,
    load_policy_model_records,
    load_policy_options,
    policy_priority,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run mathematical modeling in policy and public systems workflow.")
    parser.add_argument("--register-file", type=Path, default=Path("data/policy_model_register.csv"))
    parser.add_argument("--options-file", type=Path, default=Path("data/policy_options.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_policy_model_records(args.register_file)
    options = load_policy_options(args.options_file)

    register_rows = [
        {**asdict(record), "policy_priority": policy_priority(record)}
        for record in records
    ]
    option_rows = [evaluate_policy_option(option) for option in options]

    write_csv(tables_dir / "policy_model_register.csv", register_rows)
    write_csv(tables_dir / "policy_option_review.csv", option_rows)

    write_json(
        json_dir / "policy_decision_support_card.json",
        build_policy_decision_support_card(register_rows, option_rows),
    )

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "policy_public_systems_run.log").write_text(
        "Mathematical modeling in policy and public systems workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Policy and public systems workflow complete.")
    print(f"Records: {len(records)}")
    print(f"Options: {len(options)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
