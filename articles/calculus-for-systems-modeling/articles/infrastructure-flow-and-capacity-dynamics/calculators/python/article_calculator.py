#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json
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

def delay_value(u: float, base_delay: float = 1.0, alpha: float = 0.8) -> float:
    if u >= 1.0:
        return float("inf")
    return base_delay * (1 + alpha * (u / (1 - u)))

def build_parser():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("utilization")
    p.add_argument("--arrival", type=float, default=95.0)
    p.add_argument("--capacity", type=float, default=100.0)

    p = sub.add_parser("delay")
    p.add_argument("--utilization", type=float, default=0.95)
    p.add_argument("--base-delay", type=float, default=1.0)
    p.add_argument("--alpha", type=float, default=0.8)

    p = sub.add_parser("queue-step")
    p.add_argument("--queue", type=float, default=20.0)
    p.add_argument("--arrival", type=float, default=95.0)
    p.add_argument("--service", type=float, default=100.0)
    p.add_argument("--dt", type=float, default=1.0)

    p = sub.add_parser("bottleneck")
    p.add_argument("--capacities", default="140,120,90,130")

    p = sub.add_parser("buffer")
    p.add_argument("--inflow", type=float, default=120.0)
    p.add_argument("--outflow", type=float, default=100.0)
    p.add_argument("--capacity", type=float, default=300.0)
    p.add_argument("--time", type=float, default=24.0)

    p = sub.add_parser("capacity-decay")
    p.add_argument("--initial-capacity", type=float, default=100.0)
    p.add_argument("--maintenance", type=float, default=1.5)
    p.add_argument("--decay-rate", type=float, default=0.03)
    p.add_argument("--years", type=int, default=20)

    p = sub.add_parser("resilience")
    p.add_argument("--delivered", type=float, default=80.0)
    p.add_argument("--required", type=float, default=100.0)

    p = sub.add_parser("governance-warning")
    p.add_argument("--context", default="nominal_capacity")

    return parser

def main() -> None:
    args = build_parser().parse_args()
    cmd = args.command

    if cmd == "utilization":
        u = args.arrival / args.capacity
        emit(cmd, args, {"utilization": u, "over_capacity": u > 1.0}, "Computes demand or arrivals as a ratio of capacity.", "Peak and average demand should be documented separately.")
    elif cmd == "delay":
        d = delay_value(args.utilization, args.base_delay, args.alpha)
        emit(cmd, args, {"delay": d}, "Computes illustrative nonlinear delay as utilization approaches capacity.", "Delay functions are model assumptions and should be calibrated.")
    elif cmd == "queue-step":
        served = min(args.queue + args.arrival * args.dt, args.service * args.dt)
        next_queue = max(0.0, args.queue + args.arrival * args.dt - served)
        emit(cmd, args, {"served": served, "next_queue": next_queue}, "Computes one queue-balance step.", "Queue dynamics depend on arrival, service, and queue discipline.")
    elif cmd == "bottleneck":
        capacities = [float(x.strip()) for x in args.capacities.split(",") if x.strip()]
        eff = min(capacities)
        stage = capacities.index(eff) + 1
        emit(cmd, args, {"effective_capacity": eff, "bottleneck_stage": stage}, "Computes effective capacity for a simple series process.", "Effective capacity is limited by the smallest stage capacity.")
    elif cmd == "buffer":
        final_buffer = max(0.0, min(args.capacity, (args.inflow - args.outflow) * args.time))
        emit(cmd, args, {"final_buffer": final_buffer, "saturated": final_buffer >= args.capacity}, "Computes simplified buffer accumulation and saturation.", "Buffers can saturate under sustained imbalance.")
    elif cmd == "capacity-decay":
        capacity = args.initial_capacity
        for _ in range(args.years):
            capacity = max(0.0, capacity + args.maintenance - args.decay_rate * capacity)
        emit(cmd, args, {"final_capacity": capacity}, "Computes capacity after maintenance and decay.", "Capacity should not be assumed fixed without maintenance records.")
    elif cmd == "resilience":
        ratio = args.delivered / args.required if args.required else 0.0
        emit(cmd, args, {"service_resilience_ratio": ratio}, "Computes service delivered as a fraction of required service.", "Service resilience should be interpreted with stress conditions and equity context.")
    elif cmd == "governance-warning":
        notes = {
            "nominal_capacity": "Nominal capacity may differ from effective capacity.",
            "queue": "Average throughput can hide waiting-time and backlog effects.",
            "maintenance": "Capacity should not be assumed fixed without maintenance records.",
            "resilience": "Spare capacity may be essential resilience, not waste.",
            "equity": "Total throughput can hide unequal delay or access."
        }
        emit(cmd, args, {"note": notes.get(args.context, "Document infrastructure governance assumptions explicitly.")}, "Creates an infrastructure-governance warning.", "Infrastructure conclusions should not exceed flow definitions, capacity evidence, operating conditions, uncertainty, governance feasibility, and tested scope.")
    else:
        raise ValueError(cmd)

if __name__ == "__main__":
    main()
