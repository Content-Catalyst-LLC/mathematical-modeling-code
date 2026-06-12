from __future__ import annotations
from dataclasses import asdict, dataclass
from pathlib import Path
import csv, json
from statistics import mean

@dataclass(frozen=True)
class ModelComponent:
    symbol: str; name: str; component_type: str; role: str; unit_or_domain: str; source_or_rationale: str; review_question: str; status: str

@dataclass(frozen=True)
class ResourceScenario:
    name: str; initial_stock: float; capacity: float; inflow: float; demand: float; loss_rate: float; periods: int; description: str = ""

def validate_scenario(s: ResourceScenario) -> None:
    if s.initial_stock < 0: raise ValueError("initial_stock must be nonnegative")
    if s.capacity <= 0: raise ValueError("capacity must be positive")
    if s.initial_stock > s.capacity: raise ValueError("initial_stock cannot exceed capacity")
    if s.inflow < 0 or s.demand < 0: raise ValueError("inflow and demand must be nonnegative")
    if not 0 <= s.loss_rate <= 1: raise ValueError("loss_rate must be between 0 and 1")
    if s.periods < 1: raise ValueError("periods must be at least 1")

def bounded_update(raw_next: float, capacity: float) -> float:
    return min(capacity, max(0.0, raw_next))

def simulate_resource(s: ResourceScenario) -> list[dict[str, object]]:
    validate_scenario(s); stock = s.initial_stock; rows = []
    for period in range(s.periods + 1):
        losses = s.loss_rate * stock
        raw_next = stock + s.inflow - s.demand - losses
        constrained_next = bounded_update(raw_next, s.capacity)
        rows.append({
            "scenario": s.name, "period": period, "stock": round(stock,8),
            "inflow": s.inflow, "demand": s.demand, "losses": round(losses,8),
            "raw_next_stock": round(raw_next,8), "constrained_next_stock": round(constrained_next,8),
            "shortage": round(max(0.0, -raw_next),8), "overflow": round(max(0.0, raw_next - s.capacity),8),
            "capacity": s.capacity, "stock_margin": round(stock / s.capacity,8)
        })
        stock = constrained_next
    return rows

def summarize_resource(rows: list[dict[str, object]]) -> dict[str, object]:
    stocks = [float(r["stock"]) for r in rows]
    shortages = [float(r["shortage"]) for r in rows]
    overflows = [float(r["overflow"]) for r in rows]
    return {"scenario": rows[0]["scenario"], "final_stock": round(stocks[-1],8), "mean_stock": round(mean(stocks),8), "min_stock": min(stocks), "max_stock": max(stocks), "shortage_periods": sum(x>0 for x in shortages), "overflow_periods": sum(x>0 for x in overflows), "total_shortage": round(sum(shortages),8), "total_overflow": round(sum(overflows),8)}

def component_risk_score(c: ModelComponent) -> float:
    score = {"active":1.0,"review":5.0,"revise":8.0,"archive":2.0}.get(c.status.lower(),4.0)
    if c.component_type in {"parameter","constraint_parameter"}: score += 2.0
    if "constraint" in c.component_type: score += 1.0
    if any(t in c.review_question.lower() for t in ["sensitive","uncertain","adaptive","theoretical","represent"]): score += 0.75
    return round(score, 3)

def load_components(path: Path) -> list[ModelComponent]:
    with path.open() as f: return [ModelComponent(**row) for row in csv.DictReader(f)]

def load_scenarios(path: Path) -> list[ResourceScenario]:
    out=[]
    with path.open() as f:
        for r in csv.DictReader(f): out.append(ResourceScenario(r["scenario"], float(r["initial_stock"]), float(r["capacity"]), float(r["inflow"]), float(r["demand"]), float(r["loss_rate"]), int(r["periods"]), r.get("description", "")))
    return out

def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(payload, indent=2, sort_keys=True))

def build_component_audit_card(components, summaries):
    comp_rows=[{**asdict(c), "component_risk_score": component_risk_score(c)} for c in components]
    return {"article":"Variables, Parameters, and Constraints", "formal_model":"S[t+1]=min(K,max(0,S[t]+I[t]-D[t]-lambda*S[t]))", "components":comp_rows, "scenario_summaries":summaries, "constraint_checks":["nonnegative storage","capacity bound","loss-rate domain","nonnegative inflow and demand","shortage and overflow tracked separately"]}
