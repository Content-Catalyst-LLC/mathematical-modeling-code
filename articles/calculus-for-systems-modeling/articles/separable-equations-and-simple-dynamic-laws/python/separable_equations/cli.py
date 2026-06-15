from __future__ import annotations
import argparse, csv, json, math
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass(frozen=True)
class SeparableAuditRecord:
    scenario: str; model_type: str; time: float; analytical_state: float; euler_state: float; absolute_error: float; rate_at_euler_state: float; growth_rate: float; carrying_capacity: float | None; initial_state: float; method: str; warning: str

def exponential_solution(t: float, x0: float, r: float) -> float: return x0 * math.exp(r * t)
def exponential_rate(x: float, r: float) -> float: return r * x
def logistic_solution(t: float, x0: float, r: float, capacity: float) -> float: return capacity / (1.0 + ((capacity - x0) / x0) * math.exp(-r * t))
def logistic_rate(x: float, r: float, capacity: float) -> float: return r * x * (1.0 - x / capacity)

def simulate_exponential(x0: float, r: float, dt: float, steps: int) -> list[SeparableAuditRecord]:
    x=x0; records=[]
    for n in range(steps+1):
        t=n*dt; analytical=exponential_solution(t,x0,r); rate=exponential_rate(x,r)
        records.append(SeparableAuditRecord('exponential_growth','separable_dx_dt_equals_r_x',t,analytical,x,abs(analytical-x),rate,r,None,x0,'analytical_vs_explicit_euler','Exponential growth assumes no capacity constraint.'))
        x += dt*rate
    return records

def simulate_logistic(x0: float, r: float, capacity: float, dt: float, steps: int) -> list[SeparableAuditRecord]:
    x=x0; records=[]
    for n in range(steps+1):
        t=n*dt; analytical=logistic_solution(t,x0,r,capacity); rate=logistic_rate(x,r,capacity)
        records.append(SeparableAuditRecord('logistic_growth','separable_dx_dt_equals_r_x_one_minus_x_over_K',t,analytical,x,abs(analytical-x),rate,r,capacity,x0,'analytical_vs_explicit_euler','Logistic growth assumes a fixed carrying capacity.'))
        x += dt*rate
    return records

def write_outputs(output_dir: Path, records: list[SeparableAuditRecord]) -> None:
    (output_dir/'tables').mkdir(parents=True, exist_ok=True); (output_dir/'json').mkdir(parents=True, exist_ok=True)
    rows=[asdict(r) for r in records]
    with (output_dir/'tables'/'separable_equation_audit.csv').open('w', newline='', encoding='utf-8') as h:
        w=csv.DictWriter(h, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    (output_dir/'json'/'separable_equation_audit.json').write_text(json.dumps(rows, indent=2, sort_keys=True), encoding='utf-8')

def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument('--output-dir', type=Path, default=Path('outputs')); args=p.parse_args()
    records=[]; records.extend(simulate_exponential(10.0,0.25,0.1,100)); records.extend(simulate_logistic(10.0,0.25,100.0,0.1,100))
    write_outputs(args.output_dir, records); print('Separable equation audit complete.')
if __name__ == '__main__': main()
