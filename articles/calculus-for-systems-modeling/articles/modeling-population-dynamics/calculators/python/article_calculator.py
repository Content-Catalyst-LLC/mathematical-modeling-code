#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math, random
from dataclasses import asdict, dataclass
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"

@dataclass
class CalculatorResult:
    calculator: str
    inputs: dict
    result: dict
    interpretation: str
    warning: str = ""

def ensure() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def write(name: str, payload: CalculatorResult) -> None:
    ensure()
    (OUTPUT_DIR/f"{name}.json").write_text(json.dumps(asdict(payload), indent=2, sort_keys=True), encoding="utf-8")
    flat = {"calculator": payload.calculator, "interpretation": payload.interpretation, "warning": payload.warning}
    flat.update({f"input_{k}": v for k, v in payload.inputs.items()})
    flat.update({f"result_{k}": v for k, v in payload.result.items() if not isinstance(v, list)})
    with (OUTPUT_DIR/f"{name}.csv").open("w", newline="", encoding="utf-8") as h:
        writer = csv.DictWriter(h, fieldnames=list(flat.keys())); writer.writeheader(); writer.writerow(flat)

def emit(cmd: str, args, result: dict, interpretation: str, warning: str = "") -> None:
    payload = CalculatorResult(cmd, vars(args), result, interpretation, warning)
    write(cmd.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def logistic(n0, r, k, t): return k/(1+((k-n0)/n0)*math.exp(-r*t))
def simulate(n0, derivative, dt, steps):
    n = n0
    for _ in range(steps): n = max(0.0, n + dt*derivative(n))
    return n

def parser():
    p = argparse.ArgumentParser()
    s = p.add_subparsers(dest="command", required=True)
    for name in ["exponential", "logistic", "allee", "harvesting", "stochastic", "two-patch"]:
        q = s.add_parser(name)
        if name == "two-patch":
            q.add_argument("--n1", type=float, default=100); q.add_argument("--n2", type=float, default=400); q.add_argument("--m", type=float, default=0.04)
        else:
            q.add_argument("--n0", type=float, default=100)
        q.add_argument("--r", type=float, default=0.08); q.add_argument("--k", type=float, default=1000); q.add_argument("--t", type=float, default=40)
        if name == "allee": q.add_argument("--a", type=float, default=75)
        if name == "harvesting": q.add_argument("--h", type=float, default=12)
        if name == "stochastic": q.add_argument("--sigma", type=float, default=0.12); q.add_argument("--seed", type=int, default=17)
    q = s.add_parser("leslie"); q.add_argument("--steps", type=int, default=20)
    q = s.add_parser("capacity-warning"); q.add_argument("--n", type=float, default=900); q.add_argument("--k", type=float, default=1000); q.add_argument("--margin", type=float, default=0.15)
    q = s.add_parser("identifiability-warning"); q.add_argument("--pattern", default="short_series")
    return p

def main():
    args = parser().parse_args()
    cmd = args.command
    dt = 0.1
    if cmd == "exponential":
        value = args.n0*math.exp(args.r*args.t)
        emit(cmd, args, {"population": value}, "Unconstrained exponential population model.", "Exponential growth is a baseline, not a long-run capacity model.")
    elif cmd == "logistic":
        value = logistic(args.n0,args.r,args.k,args.t)
        emit(cmd, args, {"population": value, "capacity_fraction": value/args.k}, "Capacity-limited logistic population model.", "Carrying capacity is assumption-bearing.")
    elif cmd == "allee":
        value = simulate(args.n0, lambda n: args.r*n*(1-n/args.k)*(n/args.a-1), dt, int(args.t/dt))
        emit(cmd, args, {"population": value}, "Allee-effect model with low-population threshold.", "Threshold parameters require evidence near the threshold.")
    elif cmd == "harvesting":
        value = simulate(args.n0, lambda n: args.r*n*(1-n/args.k)-args.h, dt, int(args.t/dt))
        emit(cmd, args, {"population": value}, "Logistic model with constant removal.", "Removal terms encode management assumptions.")
    elif cmd == "stochastic":
        rng = random.Random(args.seed); n = args.n0
        for _ in range(int(args.t/dt)):
            n = max(0.0, n + args.r*n*(1-n/args.k)*dt + args.sigma*n*math.sqrt(dt)*rng.gauss(0,1))
        emit(cmd, args, {"population": n}, "One stochastic logistic path.", "A single stochastic path is not a distribution.")
    elif cmd == "two-patch":
        n1, n2 = args.n1, args.n2
        for _ in range(int(args.t/dt)):
            d1 = args.r*n1*(1-n1/args.k)+args.m*(n2-n1)
            d2 = args.r*n2*(1-n2/args.k)+args.m*(n1-n2)
            n1, n2 = max(0.0,n1+dt*d1), max(0.0,n2+dt*d2)
        emit(cmd, args, {"patch1": n1, "patch2": n2, "total": n1+n2}, "Two-patch migration model.", "Migration assumptions should match geography or network structure.")
    elif cmd == "leslie":
        v = [80.0, 40.0, 20.0]
        L = [[0.0,1.2,1.8],[0.55,0.0,0.0],[0.0,0.65,0.30]]
        for _ in range(args.steps):
            v = [sum(L[i][j]*v[j] for j in range(3)) for i in range(3)]
        emit(cmd, args, {"stage1": v[0], "stage2": v[1], "stage3": v[2], "total": sum(v)}, "Stage-structured Leslie projection.", "Aggregate totals can hide population composition.")
    elif cmd == "capacity-warning":
        fraction = args.n/args.k
        emit(cmd, args, {"capacity_fraction": fraction, "near_capacity": fraction >= 1-args.margin}, "Capacity proximity check.", "K is assumption-bearing and may be uncertain.")
    elif cmd == "identifiability-warning":
        notes = {"short_series": "Different r and K values can fit early growth similarly.", "threshold": "Allee thresholds may be invisible without low-population observations.", "stochastic": "A single stochastic path is not a distribution."}
        emit(cmd, args, {"note": notes.get(args.pattern, "Document identifiability limits.")}, "Identifiability governance warning.", "A fitted curve does not automatically prove parameter meaning.")

if __name__ == "__main__":
    main()
