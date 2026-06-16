from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class ModelParameters:
    growth_rate: float
    carrying_capacity: float
    initial_stock: float
    time_step: float
    horizon: float
    parameter_note: str

@dataclass(frozen=True)
class ModelState:
    model_time: float
    stock: float

@dataclass(frozen=True)
class DiagnosticRecord:
    diagnostic_name: str
    diagnostic_status: str
    diagnostic_message: str
    review_required: bool

@dataclass(frozen=True)
class ModelOutput:
    model_use: str
    parameters: ModelParameters
    final_state: ModelState
    diagnostics: list[DiagnosticRecord]
    interpretation_warning: str

def validate_parameters(params: ModelParameters) -> list[str]:
    messages: list[str] = []
    if params.growth_rate <= 0:
        messages.append("growth_rate must be positive")
    if params.carrying_capacity <= 0:
        messages.append("carrying_capacity must be positive")
    if params.initial_stock <= 0:
        messages.append("initial_stock must be positive")
    if params.time_step <= 0:
        messages.append("time_step must be positive")
    if params.horizon <= 0:
        messages.append("horizon must be positive")
    return messages

def step_logistic(params: ModelParameters, state: ModelState) -> ModelState:
    x = state.stock
    dx = params.growth_rate * x * (1 - x / params.carrying_capacity)
    return ModelState(model_time=state.model_time + params.time_step, stock=x + params.time_step * dx)

def simulate(params: ModelParameters) -> list[ModelState]:
    states = [ModelState(0.0, params.initial_stock)]
    while states[-1].model_time < params.horizon:
        states.append(step_logistic(params, states[-1]))
    return states

def build_output(params: ModelParameters) -> ModelOutput:
    validation_messages = validate_parameters(params)
    states = simulate(params)
    final = states[-1]
    diagnostics = [
        DiagnosticRecord(
            diagnostic_name="parameter_validation",
            diagnostic_status="converged" if not validation_messages else "warning",
            diagnostic_message="All basic parameter checks passed." if not validation_messages else "; ".join(validation_messages),
            review_required=bool(validation_messages),
        ),
        DiagnosticRecord(
            diagnostic_name="capacity_check",
            diagnostic_status="converged" if final.stock <= params.carrying_capacity else "warning",
            diagnostic_message="Final stock remains within carrying capacity." if final.stock <= params.carrying_capacity else "Final stock exceeds carrying capacity.",
            review_required=final.stock > params.carrying_capacity,
        ),
    ]
    return ModelOutput(
        model_use="governance_review",
        parameters=params,
        final_state=final,
        diagnostics=diagnostics,
        interpretation_warning="Typed records improve structural review but do not prove empirical validity.",
    )

def write_outputs(output_dir: Path) -> None:
    params = ModelParameters(
        growth_rate=0.35,
        carrying_capacity=100.0,
        initial_stock=10.0,
        time_step=0.25,
        horizon=20.0,
        parameter_note="Synthetic teaching example for typed model governance.",
    )
    output = build_output(params)

    (output_dir / "tables").mkdir(parents=True, exist_ok=True)
    (output_dir / "json").mkdir(parents=True, exist_ok=True)
    (output_dir / "reports").mkdir(parents=True, exist_ok=True)

    summary_row = {
        "model_use": output.model_use,
        "growth_rate": output.parameters.growth_rate,
        "carrying_capacity": output.parameters.carrying_capacity,
        "initial_stock": output.parameters.initial_stock,
        "time_step": output.parameters.time_step,
        "horizon": output.parameters.horizon,
        "final_time": output.final_state.model_time,
        "final_stock": output.final_state.stock,
        "interpretation_warning": output.interpretation_warning,
    }

    with (output_dir / "tables" / "typed_model_output.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_row.keys()))
        writer.writeheader()
        writer.writerow(summary_row)

    diag_rows = [asdict(diagnostic) for diagnostic in output.diagnostics]
    with (output_dir / "tables" / "diagnostics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(diag_rows[0].keys()))
        writer.writeheader()
        writer.writerows(diag_rows)

    (output_dir / "json" / "typed_model_output.json").write_text(json.dumps(asdict(output), indent=2, sort_keys=True), encoding="utf-8")

    report_lines = [
        "# Typed Model Record Audit",
        "",
        f"Model use: {output.model_use}",
        f"Final stock: {output.final_state.stock:.6f}",
        "",
        "## Diagnostics",
    ]
    for diagnostic in output.diagnostics:
        report_lines.append(f"- **{diagnostic.diagnostic_name}** ({diagnostic.diagnostic_status}): {diagnostic.diagnostic_message}")
    report_lines.append("")
    report_lines.append(output.interpretation_warning)

    (output_dir / "reports" / "typed_model_record_audit.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    write_outputs(args.output_dir)
    print("Typed model record outputs generated.")

if __name__ == "__main__":
    main()
