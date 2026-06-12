from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from scientific_computing_modeling_workflows.core import (
    build_output_index,
    build_run_manifest,
    build_workflow_audit_card,
    load_records,
    load_scenarios,
    simulate,
    summarize_trajectories,
    workflow_risk_score,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run scientific computing modeling workflow.")
    parser.add_argument("--scenario-file", type=Path, default=Path("data/resource_workflow_scenarios.csv"))
    parser.add_argument("--register-file", type=Path, default=Path("data/scientific_computing_workflow_register.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    scenarios = load_scenarios(args.scenario_file)
    records = load_records(args.register_file)

    rows: list[dict[str, object]] = []
    for scenario in scenarios:
        rows.extend(simulate(scenario))

    summary = summarize_trajectories(rows)
    register_rows = [
        {**asdict(record), "workflow_risk_score": workflow_risk_score(record)}
        for record in records
    ]

    trajectory_path = tables_dir / "resource_model_trajectories.csv"
    summary_path = tables_dir / "resource_model_summary.csv"
    register_path = tables_dir / "scientific_computing_workflow_register.csv"
    output_index_path = tables_dir / "workflow_output_index.csv"
    manifest_path = json_dir / "run_manifest.json"
    audit_path = json_dir / "workflow_audit_card.json"
    log_path = logs_dir / "workflow_run.log"

    write_csv(trajectory_path, rows)
    write_csv(summary_path, summary)
    write_csv(register_path, register_rows)

    output_paths = {
        "trajectories": trajectory_path,
        "summary": summary_path,
        "workflow_register": register_path,
    }

    write_csv(output_index_path, build_output_index(output_paths))
    output_paths["output_index"] = output_index_path

    write_json(manifest_path, build_run_manifest("Scientific Computing for Modeling Workflows", scenarios, output_paths))
    output_paths["run_manifest"] = manifest_path

    write_json(audit_path, build_workflow_audit_card(records, scenarios, summary, output_paths))
    output_paths["audit_card"] = audit_path

    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path.write_text("Scientific computing modeling workflow completed successfully.\n", encoding="utf-8")

    print("Scientific computing modeling workflow complete.")
    print(f"Workflow records: {len(records)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
