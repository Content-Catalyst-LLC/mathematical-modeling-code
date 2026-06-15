from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class SeriesAudit:
    series_name: str
    n_terms: int
    last_term: float
    partial_sum: float
    reference_value: float | None
    estimated_error: float | None
    convergence_classification: str
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


def audit_geometric(a: float, r: float, n_terms: int) -> SeriesAudit:
    terms = geometric_terms(a, r, n_terms)
    partial_sum = sum(terms)

    reference = None
    error = None
    classification = "divergent or inconclusive"
    warning = ""

    if abs(r) < 1:
        reference = a / (1 - r)
        error = reference - partial_sum
        classification = "convergent geometric series"
    else:
        warning = "geometric ratio does not support convergence"

    return SeriesAudit(
        series_name="geometric",
        n_terms=n_terms,
        last_term=terms[-1],
        partial_sum=partial_sum,
        reference_value=reference,
        estimated_error=error,
        convergence_classification=classification,
        stopping_rule="fixed term count with analytic tail check",
        warning=warning,
    )


def audit_harmonic(n_terms: int) -> SeriesAudit:
    terms = harmonic_terms(n_terms)
    return SeriesAudit(
        series_name="harmonic",
        n_terms=n_terms,
        last_term=terms[-1],
        partial_sum=sum(terms),
        reference_value=None,
        estimated_error=None,
        convergence_classification="divergent despite terms approaching zero",
        stopping_rule="fixed term count; no finite limiting total",
        warning="small last term does not imply finite accumulated total",
    )


def audit_p_series(p: float, n_terms: int) -> SeriesAudit:
    terms = p_series_terms(p, n_terms)
    classification = "convergent p-series" if p > 1 else "divergent p-series"
    warning = "" if p > 1 else "p-series diverges for p <= 1 even though terms may approach zero"

    return SeriesAudit(
        series_name=f"p_series_p_{p:g}",
        n_terms=n_terms,
        last_term=terms[-1],
        partial_sum=sum(terms),
        reference_value=None,
        estimated_error=None,
        convergence_classification=classification,
        stopping_rule="fixed term count with p-series classification",
        warning=warning,
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
