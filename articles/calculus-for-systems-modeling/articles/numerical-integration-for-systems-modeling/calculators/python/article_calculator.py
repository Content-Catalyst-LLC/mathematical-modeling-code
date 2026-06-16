#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
from pathlib import Path
OUT = Path(__file__).resolve().parents[1] / "outputs"
def rate(t): return 2.0 + math.sin(t) + 0.1*t
def trueint(t): return 2.0*t - math.cos(t) + 1.0 + 0.05*t*t
def save(name, payload):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    flat = {"calculator": payload["calculator"]}
    flat.update(payload.get("result", {}))
    with (OUT / f"{name}.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(flat.keys()))
        w.writeheader()
        w.writerow(flat)
parser = argparse.ArgumentParser()
sub = parser.add_subparsers(dest="command", required=True)
p=sub.add_parser("left-rectangle"); p.add_argument("--rate-left", type=float, default=3.2); p.add_argument("--h", type=float, default=0.25)
p=sub.add_parser("trapezoid-step"); p.add_argument("--rate-left", type=float, default=3.0); p.add_argument("--rate-right", type=float, default=4.0); p.add_argument("--h", type=float, default=0.25)
p=sub.add_parser("simpson-one-third"); p.add_argument("--f0", type=float, default=2.0); p.add_argument("--f1", type=float, default=3.0); p.add_argument("--f2", type=float, default=2.0); p.add_argument("--h", type=float, default=0.5)
p=sub.add_parser("benchmark-audit"); p.add_argument("--start", type=float, default=0.0); p.add_argument("--stop", type=float, default=10.0); p.add_argument("--h", type=float, default=0.1)
p=sub.add_parser("conservation-check"); p.add_argument("--initial-stock", type=float, default=100.0); p.add_argument("--final-stock", type=float, default=130.0); p.add_argument("--integrated-inflow", type=float, default=50.0); p.add_argument("--integrated-outflow", type=float, default=20.0)
args = parser.parse_args()
cmd = args.command
if cmd == "left-rectangle":
    result = {"contribution": args.rate_left * args.h}
elif cmd == "trapezoid-step":
    result = {"contribution": 0.5*(args.rate_left+args.rate_right)*args.h}
elif cmd == "simpson-one-third":
    result = {"contribution": (args.h/3.0)*(args.f0 + 4.0*args.f1 + args.f2)}
elif cmd == "benchmark-audit":
    h=args.h; n=int(round((args.stop-args.start)/h)); left=0.0; trap=0.0; rows=[]
    for i in range(n+1):
        t=args.start+i*h; r=rate(t)
        if i>0:
            left += rate(args.start+(i-1)*h)*h
            trap += 0.5*(rate(args.start+(i-1)*h)+r)*h
        truth=trueint(t)-trueint(args.start)
        rows.append({"index":i,"time":t,"rate":r,"left_cumulative":left,"trapezoid_cumulative":trap,"true_cumulative":truth,"trapezoid_absolute_error":abs(trap-truth)})
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/"benchmark_audit.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    with (OUT/"benchmark_audit.csv").open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    result={"records":len(rows),"final_trapezoid_cumulative":rows[-1]["trapezoid_cumulative"],"final_true_cumulative":rows[-1]["true_cumulative"],"final_trapezoid_absolute_error":rows[-1]["trapezoid_absolute_error"]}
elif cmd == "conservation-check":
    observed=args.final_stock-args.initial_stock
    modeled=args.integrated_inflow-args.integrated_outflow
    result={"observed_stock_change":observed,"modeled_net_flow":modeled,"conservation_residual":observed-modeled}
payload={"calculator":cmd,"inputs":vars(args),"result":result,"warning":"Numerical integration estimates depend on integrand meaning, units, spacing, rule choice, missing data, and interpretation scope."}
save(cmd.replace("-","_"), payload)
print(json.dumps(payload, indent=2, sort_keys=True))
