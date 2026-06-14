from __future__ import annotations

import argparse
from dataclasses import asdict
from pathlib import Path
import sys

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from communicating_model_uncertainty.core import (
    build_communication_card,
    communication_priority,
    load_communication_records,
    load_uncertainty_messages,
    write_csv,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run model uncertainty communication workflow.")
    parser.add_argument("--records-file", type=Path, default=Path("data/communication_records.csv"))
    parser.add_argument("--messages-file", type=Path, default=Path("data/uncertainty_messages.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tables_dir = args.output_dir / "tables"
    json_dir = args.output_dir / "json"
    logs_dir = args.output_dir / "logs"

    records = load_communication_records(args.records_file)
    messages = load_uncertainty_messages(args.messages_file)

    record_rows = [
        {**asdict(record), "communication_priority": communication_priority(record)}
        for record in records
    ]

    write_csv(tables_dir / "communication_review_queue.csv", record_rows)
    write_csv(tables_dir / "uncertainty_messages.csv", [asdict(message) for message in messages])
    write_json(json_dir / "uncertainty_communication_card.json", build_communication_card(records, messages))

    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "communication_run.log").write_text(
        "Model uncertainty communication workflow completed successfully.\n",
        encoding="utf-8",
    )

    print("Model uncertainty communication workflow complete.")
    print(f"Records: {len(records)}")
    print(f"Messages: {len(messages)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
