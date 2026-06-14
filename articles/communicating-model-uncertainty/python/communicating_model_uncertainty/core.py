from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import csv
import json


@dataclass(frozen=True)
class CommunicationRecord:
    key: str
    communication_layer: str
    audience: str
    message_goal: str
    plain_language_statement: str
    status: str


@dataclass(frozen=True)
class UncertaintyMessage:
    key: str
    uncertainty_type: str
    technical_statement: str
    plain_language_statement: str
    decision_relevance: str


def load_communication_records(path: Path) -> list[CommunicationRecord]:
    records: list[CommunicationRecord] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            records.append(
                CommunicationRecord(
                    key=row["key"],
                    communication_layer=row["communication_layer"],
                    audience=row["audience"],
                    message_goal=row["message_goal"],
                    plain_language_statement=row["plain_language_statement"],
                    status=row["status"],
                )
            )
    if not records:
        raise ValueError("Communication records table cannot be empty.")
    return records


def load_uncertainty_messages(path: Path) -> list[UncertaintyMessage]:
    messages: list[UncertaintyMessage] = []
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            messages.append(
                UncertaintyMessage(
                    key=row["key"],
                    uncertainty_type=row["uncertainty_type"],
                    technical_statement=row["technical_statement"],
                    plain_language_statement=row["plain_language_statement"],
                    decision_relevance=row["decision_relevance"],
                )
            )
    if not messages:
        raise ValueError("Uncertainty messages table cannot be empty.")
    return messages


def communication_priority(record: CommunicationRecord) -> float:
    score = {"active": 1.0, "review": 5.0, "revise": 8.0, "archive": 2.0}.get(
        record.status.lower(),
        4.0,
    )
    text = f"{record.communication_layer} {record.audience} {record.message_goal}".lower()
    for term in ["threshold", "decision", "limit", "public", "governance", "uncertainty"]:
        if term in text:
            score += 1.0
    return round(score, 8)


def build_communication_card(
    records: list[CommunicationRecord],
    messages: list[UncertaintyMessage],
) -> dict[str, object]:
    return {
        "article": "Communicating Model Uncertainty",
        "core_principle": "Model outputs are conditional claims; communication should make uncertainty, assumptions, limits, and decision relevance visible.",
        "communication_records": [
            {**asdict(record), "communication_priority": communication_priority(record)}
            for record in records
        ],
        "uncertainty_messages": [asdict(message) for message in messages],
        "use_limit_statement": "This model supports interpretation and decision support only within its stated assumptions, validation domain, uncertainty assessment, and use context.",
        "audience_guidance": {
            "technical_reviewer": "Provide methods, assumptions, diagnostics, validation scope, and reproducibility materials.",
            "decision_maker": "Emphasize threshold risk, robustness, fragility, consequences, and monitoring needs.",
            "public": "Use plain-language ranges, scenario labels, and clear limits without false certainty.",
            "future_user": "State use limits, update triggers, and uncertainty sources that require monitoring.",
        },
        "diagnostic_checks": [
            "uncertainty sources are named",
            "intervals and ranges are labeled",
            "scenarios are not misrepresented as forecasts",
            "threshold risk is communicated",
            "structural uncertainty is not hidden",
            "use limits are stated",
        ],
    }


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)
