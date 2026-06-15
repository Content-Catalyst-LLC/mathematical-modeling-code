from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class ConvergenceTestAudit:
    series_name: str
    test_used: str
    n_terms: int
    partial_sum: float
    last_term: float
    test_result: str
    estimated_error: float | None
    stopping_rule: str
    warning: str


def geometric_terms(a: float, r: float, n_terms: int) -> list[float]:
    if n_terms <= 0:
        raise ValueError("n_terms must be positive.")
    return [a * (r ** n) for n in range(n_terms)]


def harmonic_terms(n_terms: int) -> list[float]:
    if n_terms <= 0:
        raise ValueError("n_terms must be positive.")
    return [1.0 / n for n in range(1, n_terms + 1)]


def p_series_terms(p: float, n_terms: int) -> list[float]:
    if n_terms <= 0:
        raise ValueError("n_terms must be positive.")
    return [1.0 / (n ** p) for n in range(1, n_terms + 1)]


def alternating_harmonic_terms(n_terms: int) -> list[float]:
    if n_terms <= 0:
        raise ValueError("n_terms must be positive.")
    return [((-1.0) ** (n + 1)) / n for n in range(1, n_terms + 1)]


def audit_geometric(a: float, r: float, n_terms: int) -> ConvergenceTestAudit:
    terms = geometric_terms(a, r, n_terms)
    partial = sum(terms)

    if abs(r) < 1:
        reference = a / (1 - r)
        error = reference - partial
        result = "converges by geometric-series test"
        warning = ""
    else:
        error = None
        result = "diverges or lacks geometric convergence"
        warning = "ratio magnitude is not below one"

    return ConvergenceTestAudit(
        series_name=f"geometric_r_{r:g}",
        test_used="geometric-series test",
        n_terms=n_terms,
        partial_sum=partial,
        last_term=terms[-1],
        test_result=result,
        estimated_error=error,
        stopping_rule="fixed term count with geometric tail check",
        warning=warning,
    )


def audit_harmonic(n_terms: int) -> ConvergenceTestAudit:
    terms = harmonic_terms(n_terms)
    return ConvergenceTestAudit(
        series_name="harmonic",
        test_used="p-series test with p=1",
        n_terms=n_terms,
        partial_sum=sum(terms),
        last_term=terms[-1],
        test_result="diverges",
        estimated_error=None,
        stopping_rule="fixed term count; no finite infinite-total claim",
        warning="terms approach zero but the series diverges",
    )


def audit_p_series(p: float, n_terms: int) -> ConvergenceTestAudit:
    terms = p_series_terms(p, n_terms)
    converges = p > 1.0

    return ConvergenceTestAudit(
        series_name=f"p_series_{p:g}",
        test_used="p-series test",
        n_terms=n_terms,
        partial_sum=sum(terms),
        last_term=terms[-1],
        test_result="converges" if converges else "diverges",
        estimated_error=None,
        stopping_rule="fixed term count with p-series classification",
        warning="" if converges else "p-series diverges for p less than or equal to one",
    )


def audit_alternating_harmonic(n_terms: int) -> ConvergenceTestAudit:
    terms = alternating_harmonic_terms(n_terms)
    next_term_bound = 1.0 / (n_terms + 1)
    return ConvergenceTestAudit(
        series_name="alternating_harmonic",
        test_used="alternating-series test",
        n_terms=n_terms,
        partial_sum=sum(terms),
        last_term=terms[-1],
        test_result="converges conditionally",
        estimated_error=next_term_bound,
        stopping_rule="fixed term count with alternating-series next-term error bound",
        warning="net convergence depends on sign cancellation; absolute series diverges",
    )


def to_dicts(rows: list[object]) -> list[dict[str, object]]:
    return [asdict(row) for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows to write: {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
