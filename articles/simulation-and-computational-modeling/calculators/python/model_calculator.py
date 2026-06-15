#!/usr/bin/env python3
"""
Self-contained model calculator for article companion repositories.

No third-party packages required. Designed for quick command-line use in
calculus, systems modeling, differential equations, sensitivity, scaling,
and numerical approximation examples.

Examples:
  python model_calculator.py derivative --expr "sin(x)*exp(-x)" --x 1.5
  python model_calculator.py integral --expr "x*x + sin(x)" --a 0 --b 10 --method simpson --n 1000
  python model_calculator.py euler --ode "0.2*y*(1-y/100)" --y0 10 --t0 0 --dt 0.1 --steps 50
  python model_calculator.py rk4 --ode "0.2*y*(1-y/100)" --y0 10 --t0 0 --dt 0.1 --steps 50
  python model_calculator.py logistic --r 0.2 --k 100 --y0 10 --dt 0.1 --steps 50
  python model_calculator.py finite-difference --values "1,1.4,2.1,3.2" --h 0.5
  python model_calculator.py sensitivity --expr "r*x*(1-x/k)" --param r --min 0.05 --max 0.5 --count 10 --x 25 --params "k=100"
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from typing import Callable, Dict, Iterable, List, Tuple

SAFE_NAMES: Dict[str, float | Callable[..., float]] = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("_")
}
SAFE_NAMES.update({"abs": abs, "min": min, "max": max, "pow": pow})


def parse_params(raw: str | None) -> Dict[str, float]:
    params: Dict[str, float] = {}
    if not raw:
        return params
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "=" not in chunk:
            raise ValueError(f"Parameter '{chunk}' must use name=value format")
        key, value = chunk.split("=", 1)
        key = key.strip()
        if not key.isidentifier():
            raise ValueError(f"Invalid parameter name: {key!r}")
        params[key] = float(value)
    return params


def safe_eval(expr: str, **values: float) -> float:
    local_scope = dict(SAFE_NAMES)
    local_scope.update(values)
    try:
        return float(eval(expr, {"__builtins__": {}}, local_scope))
    except Exception as exc:  # pragma: no cover - command-line diagnostics
        raise ValueError(f"Could not evaluate expression {expr!r}: {exc}") from exc


def write_rows(rows: Iterable[Dict[str, float]], out_path: str | None = None) -> None:
    rows = list(rows)
    if not rows:
        return
    handle = open(out_path, "w", newline="", encoding="utf-8") if out_path else sys.stdout
    close_handle = out_path is not None
    try:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    finally:
        if close_handle:
            handle.close()


def derivative(args: argparse.Namespace) -> None:
    params = parse_params(args.params)
    x = args.x
    h = args.h
    f = lambda z: safe_eval(args.expr, x=z, t=args.t, **params)
    if args.method == "central":
        value = (f(x + h) - f(x - h)) / (2 * h)
    elif args.method == "forward":
        value = (f(x + h) - f(x)) / h
    elif args.method == "backward":
        value = (f(x) - f(x - h)) / h
    else:
        raise ValueError(f"Unknown derivative method: {args.method}")
    print(f"derivative,{value:.12g}")


def integral(args: argparse.Namespace) -> None:
    params = parse_params(args.params)
    a, b, n = args.a, args.b, max(1, args.n)
    f = lambda z: safe_eval(args.expr, x=z, t=args.t, **params)
    h = (b - a) / n
    if args.method == "midpoint":
        value = h * sum(f(a + (i + 0.5) * h) for i in range(n))
    elif args.method == "trapezoid":
        value = h * (0.5 * f(a) + sum(f(a + i * h) for i in range(1, n)) + 0.5 * f(b))
    elif args.method == "simpson":
        if n % 2 == 1:
            n += 1
            h = (b - a) / n
        odds = sum(f(a + i * h) for i in range(1, n, 2))
        evens = sum(f(a + i * h) for i in range(2, n, 2))
        value = h / 3 * (f(a) + 4 * odds + 2 * evens + f(b))
    else:
        raise ValueError(f"Unknown integration method: {args.method}")
    print(f"integral,{value:.12g}")


def ode_function(expr: str, params: Dict[str, float]) -> Callable[[float, float], float]:
    return lambda t, y: safe_eval(expr, t=t, x=t, y=y, **params)


def euler_rows(f: Callable[[float, float], float], t0: float, y0: float, dt: float, steps: int) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    t, y = t0, y0
    for step in range(steps + 1):
        rows.append({"step": step, "t": t, "y": y})
        if step < steps:
            y = y + dt * f(t, y)
            t = t + dt
    return rows


def rk4_rows(f: Callable[[float, float], float], t0: float, y0: float, dt: float, steps: int) -> List[Dict[str, float]]:
    rows: List[Dict[str, float]] = []
    t, y = t0, y0
    for step in range(steps + 1):
        rows.append({"step": step, "t": t, "y": y})
        if step < steps:
            k1 = f(t, y)
            k2 = f(t + dt / 2, y + dt * k1 / 2)
            k3 = f(t + dt / 2, y + dt * k2 / 2)
            k4 = f(t + dt, y + dt * k3)
            y = y + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
            t = t + dt
    return rows


def solve_euler(args: argparse.Namespace) -> None:
    f = ode_function(args.ode, parse_params(args.params))
    write_rows(euler_rows(f, args.t0, args.y0, args.dt, args.steps), args.out)


def solve_rk4(args: argparse.Namespace) -> None:
    f = ode_function(args.ode, parse_params(args.params))
    write_rows(rk4_rows(f, args.t0, args.y0, args.dt, args.steps), args.out)


def logistic(args: argparse.Namespace) -> None:
    r, k = args.r, args.k
    f = lambda _t, y: r * y * (1 - y / k)
    rows = rk4_rows(f, args.t0, args.y0, args.dt, args.steps)
    write_rows(rows, args.out)


def finite_difference(args: argparse.Namespace) -> None:
    values = [float(x.strip()) for x in args.values.split(",") if x.strip()]
    if len(values) < 2:
        raise ValueError("Provide at least two comma-separated values")
    h = args.h
    rows: List[Dict[str, float]] = []
    for i, value in enumerate(values):
        row: Dict[str, float] = {"index": i, "value": value}
        if i < len(values) - 1:
            row["forward_difference"] = (values[i + 1] - values[i]) / h
        else:
            row["forward_difference"] = float("nan")
        if 0 < i < len(values) - 1:
            row["central_difference"] = (values[i + 1] - values[i - 1]) / (2 * h)
        else:
            row["central_difference"] = float("nan")
        rows.append(row)
    write_rows(rows, args.out)


def sensitivity(args: argparse.Namespace) -> None:
    params = parse_params(args.params)
    if args.count < 2:
        raise ValueError("--count must be at least 2")
    rows: List[Dict[str, float]] = []
    for i in range(args.count):
        value = args.min + (args.max - args.min) * i / (args.count - 1)
        local_params = dict(params)
        local_params[args.param] = value
        output = safe_eval(args.expr, x=args.x, t=args.t, y=args.y, **local_params)
        rows.append({"index": i, args.param: value, "output": output})
    write_rows(rows, args.out)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Self-contained calculator for article companion models")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("derivative", help="Estimate derivative of an expression in x")
    p.add_argument("--expr", required=True, help="Expression in x, e.g. sin(x)*exp(-x)")
    p.add_argument("--x", type=float, required=True, help="Evaluation point")
    p.add_argument("--h", type=float, default=1e-5, help="Step size")
    p.add_argument("--t", type=float, default=0.0, help="Optional time value")
    p.add_argument("--params", default="", help="Comma-separated parameters, e.g. r=0.2,k=100")
    p.add_argument("--method", choices=["central", "forward", "backward"], default="central")
    p.set_defaults(func=derivative)

    p = sub.add_parser("integral", help="Estimate definite integral of an expression in x")
    p.add_argument("--expr", required=True)
    p.add_argument("--a", type=float, required=True)
    p.add_argument("--b", type=float, required=True)
    p.add_argument("--n", type=int, default=1000)
    p.add_argument("--t", type=float, default=0.0)
    p.add_argument("--params", default="")
    p.add_argument("--method", choices=["trapezoid", "midpoint", "simpson"], default="simpson")
    p.set_defaults(func=integral)

    for name, fn in [("euler", solve_euler), ("rk4", solve_rk4)]:
        p = sub.add_parser(name, help=f"Solve dy/dt = f(t,y) with {name.upper()}")
        p.add_argument("--ode", required=True, help="Expression in t and y, e.g. 0.2*y*(1-y/100)")
        p.add_argument("--y0", type=float, required=True)
        p.add_argument("--t0", type=float, default=0.0)
        p.add_argument("--dt", type=float, default=0.1)
        p.add_argument("--steps", type=int, default=50)
        p.add_argument("--params", default="")
        p.add_argument("--out", default=None, help="Optional CSV output path")
        p.set_defaults(func=fn)

    p = sub.add_parser("logistic", help="Simulate logistic growth with RK4")
    p.add_argument("--r", type=float, required=True)
    p.add_argument("--k", type=float, required=True)
    p.add_argument("--y0", type=float, required=True)
    p.add_argument("--t0", type=float, default=0.0)
    p.add_argument("--dt", type=float, default=0.1)
    p.add_argument("--steps", type=int, default=50)
    p.add_argument("--out", default=None)
    p.set_defaults(func=logistic)

    p = sub.add_parser("finite-difference", help="Compute finite differences from comma-separated values")
    p.add_argument("--values", required=True)
    p.add_argument("--h", type=float, default=1.0)
    p.add_argument("--out", default=None)
    p.set_defaults(func=finite_difference)

    p = sub.add_parser("sensitivity", help="Evaluate expression over a parameter sweep")
    p.add_argument("--expr", required=True)
    p.add_argument("--param", required=True)
    p.add_argument("--min", type=float, required=True)
    p.add_argument("--max", type=float, required=True)
    p.add_argument("--count", type=int, default=11)
    p.add_argument("--x", type=float, default=1.0)
    p.add_argument("--y", type=float, default=1.0)
    p.add_argument("--t", type=float, default=0.0)
    p.add_argument("--params", default="")
    p.add_argument("--out", default=None)
    p.set_defaults(func=sensitivity)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
