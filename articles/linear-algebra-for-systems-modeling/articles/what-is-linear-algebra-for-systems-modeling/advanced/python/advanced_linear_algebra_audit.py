from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class AdvancedAuditItem:
    audit_key: str
    audit_name: str
    modeling_question: str
    review_warning: str

ITEMS = [
    AdvancedAuditItem("state_vector", "State Vector", "What does each vector component represent?", "Missing units or ordering can invalidate interpretation."),
    AdvancedAuditItem("matrix_semantics", "Matrix Semantics", "What do matrix entries mean?", "A valid operation may be meaningless if entries are not semantically defined."),
    AdvancedAuditItem("rank_dependency", "Rank and Dependency", "Is structure independent, redundant, or underdetermined?", "Rank is a diagnostic, not a substitute for model judgment."),
    AdvancedAuditItem("eigen_claims", "Eigenvalue Claims", "Is stability or long-run behavior being inferred correctly?", "Eigenstructure depends on model form, scaling, and linearity assumptions."),
    AdvancedAuditItem("reduction_loss", "Reduction Loss", "What does dimensionality reduction preserve or discard?", "Clean components can hide important variation."),
]

def write_outputs(output_dir: Path) -> None:
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)
    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    rows = [asdict(item) for item in ITEMS]
    with (output_dir / "tables" / "advanced_linear_algebra_audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "json" / "advanced_linear_algebra_audit.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    lines = ["# Advanced Linear Algebra Modeling Audit\n"]
    for item in ITEMS:
        lines.append(f"## {item.audit_name}\n")
        lines.append(f"- Question: {item.modeling_question}")
        lines.append(f"- Warning: {item.review_warning}\n")
    (output_dir / "reports" / "advanced_linear_algebra_audit.md").write_text("\n".join(lines), encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Advanced linear algebra audit generated.")

if __name__ == "__main__":
    main()
