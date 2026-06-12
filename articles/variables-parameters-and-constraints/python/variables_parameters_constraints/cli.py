from __future__ import annotations
import argparse, sys
from dataclasses import asdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from variables_parameters_constraints.core import *

def main():
    p=argparse.ArgumentParser(); p.add_argument("--component-file", type=Path, default=Path("data/component_register.csv")); p.add_argument("--scenario-file", type=Path, default=Path("data/component_scenarios.csv")); p.add_argument("--output-dir", type=Path, default=Path("outputs")); args=p.parse_args()
    tables=args.output_dir/"tables"; json_dir=args.output_dir/"json"
    components=load_components(args.component_file); scenarios=load_scenarios(args.scenario_file)
    all_rows=[]; summary_rows=[]
    for s in scenarios:
        rows=simulate_resource(s); all_rows.extend(rows); summary=summarize_resource(rows); summary["description"]=s.description; summary_rows.append(summary)
    component_rows=[{**asdict(c), "component_risk_score": component_risk_score(c)} for c in components]
    write_csv(tables/"component_scenario_timeseries.csv", all_rows)
    write_csv(tables/"component_scenario_summary.csv", summary_rows)
    write_csv(tables/"component_register.csv", component_rows)
    write_json(json_dir/"component_audit_card.json", build_component_audit_card(components, summary_rows))
    print("Variables, parameters, and constraints workflow complete.")
    print(f"Components: {len(components)}")
    print(f"Scenarios: {len(scenarios)}")
    print(f"Outputs: {args.output_dir}")
if __name__ == "__main__": main()
