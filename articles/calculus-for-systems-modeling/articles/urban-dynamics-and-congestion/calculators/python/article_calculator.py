#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, math
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

def parse_float_list(value: str) -> list[float]:
    return [float(part.strip()) for part in value.split(",") if part.strip()]

def write(name: str, payload: CalculatorResult) -> None:
    ensure()
    (OUTPUT_DIR / f"{name}.json").write_text(json.dumps(asdict(payload), indent=2, sort_keys=True), encoding="utf-8")
    flat = {"calculator": payload.calculator, "interpretation": payload.interpretation, "warning": payload.warning}
    flat.update({f"input_{k}": v for k, v in payload.inputs.items()})
    flat.update({f"result_{k}": v for k, v in payload.result.items() if not isinstance(v, list)})
    with (OUTPUT_DIR / f"{name}.csv").open("w", newline="", encoding="utf-8") as h:
        writer = csv.DictWriter(h, fieldnames=list(flat.keys()))
        writer.writeheader()
        writer.writerow(flat)

def emit(cmd: str, args, result: dict, interpretation: str, warning: str = "") -> None:
    payload = CalculatorResult(cmd, vars(args), result, interpretation, warning)
    write(cmd.replace("-", "_"), payload)
    print(json.dumps(asdict(payload), indent=2, sort_keys=True))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("traffic-flow")
    p.add_argument("--density", type=float, default=35.0)
    p.add_argument("--free-flow-speed", type=float, default=60.0)
    p.add_argument("--jam-density", type=float, default=140.0)

    p = sub.add_parser("critical-density")
    p.add_argument("--jam-density", type=float, default=140.0)

    p = sub.add_parser("queue-step")
    p.add_argument("--queue", type=float, default=0.0)
    p.add_argument("--arrival-rate", type=float, default=2300.0)
    p.add_argument("--service-rate", type=float, default=2000.0)
    p.add_argument("--dt", type=float, default=0.01)

    p = sub.add_parser("bpr-travel-time")
    p.add_argument("--free-flow-time", type=float, default=20.0)
    p.add_argument("--volume", type=float, default=2300.0)
    p.add_argument("--capacity", type=float, default=2000.0)
    p.add_argument("--alpha", type=float, default=0.15)
    p.add_argument("--beta", type=float, default=4.0)

    p = sub.add_parser("accessibility")
    p.add_argument("--opportunities", default="1000,500,250")
    p.add_argument("--travel-times", default="10,25,45")
    p.add_argument("--theta", type=float, default=0.08)

    p = sub.add_parser("induced-demand-step")
    p.add_argument("--volume", type=float, default=2300.0)
    p.add_argument("--target-volume", type=float, default=2600.0)
    p.add_argument("--adjustment-rate", type=float, default=0.15)
    p.add_argument("--dt", type=float, default=1.0)

    p = sub.add_parser("distributional-delay")
    p.add_argument("--delays", default="10,20,35")
    p.add_argument("--weights", default="1,1.5,2")

    p = sub.add_parser("governance-warning")
    p.add_argument("--context", default="equity")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "traffic-flow":
        flow = max(0.0, args.free_flow_speed * args.density * (1 - args.density / args.jam_density))
        emit(cmd, args, {"flow": flow}, "Computes flow from density, free-flow speed, and jam density.", "Fundamental diagrams are context-specific, not universal laws.")
    elif cmd == "critical-density":
        emit(cmd, args, {"critical_density": args.jam_density / 2}, "Computes critical density in the simple parabolic model.", "Critical density depends on the selected flow-density relation.")
    elif cmd == "queue-step":
        next_queue = max(0.0, args.queue + (args.arrival_rate - args.service_rate) * args.dt)
        emit(cmd, args, {"next_queue": next_queue}, "Computes one queue accumulation step.", "Over-capacity delays can spill back upstream.")
    elif cmd == "bpr-travel-time":
        travel_time = args.free_flow_time * (1 + args.alpha * (args.volume / args.capacity) ** args.beta)
        emit(cmd, args, {"travel_time": travel_time, "delay": travel_time - args.free_flow_time}, "Computes BPR travel time.", "Travel-time functions should be calibrated and not treated as universal.")
    elif cmd == "accessibility":
        opportunities = parse_float_list(args.opportunities)
        travel_times = parse_float_list(args.travel_times)
        value = sum(o * math.exp(-args.theta * t) for o, t in zip(opportunities, travel_times))
        emit(cmd, args, {"accessibility": value}, "Computes an exponential-decay accessibility measure.", "Accessibility depends on opportunity definition and travel-cost assumptions.")
    elif cmd == "induced-demand-step":
        value = args.volume + args.adjustment_rate * (args.target_volume - args.volume) * args.dt
        emit(cmd, args, {"next_volume": value}, "Computes one induced-demand adjustment step.", "Fixed-demand assumptions can mislead in long-run planning.")
    elif cmd == "distributional-delay":
        delays = parse_float_list(args.delays)
        weights = parse_float_list(args.weights)
        value = sum(d * w for d, w in zip(delays, weights))
        emit(cmd, args, {"distributional_delay_burden": value}, "Computes weighted delay burden.", "Average travel-time improvements can hide unequal burden or local harm.")
    elif cmd == "governance-warning":
        notes = {
            "boundary": "Urban congestion conclusions are not meaningful without a defined boundary and spillover context.",
            "vehicle_flow": "Vehicle flow should not be treated as the only mobility outcome.",
            "capacity": "Capacity depends on design, operations, behavior, incidents, and curb use.",
            "fixed_demand": "Fixed-demand assumptions can mislead in long-run planning.",
            "equity": "Average travel-time improvements can hide unequal burden or local harm."
        }
        emit(cmd, args, {"note": notes.get(args.context, "Document urban modeling assumptions explicitly.")}, "Creates an urban modeling governance warning.", "Urban conclusions should not exceed boundary definitions, data evidence, behavioral assumptions, uncertainty, equity review, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
