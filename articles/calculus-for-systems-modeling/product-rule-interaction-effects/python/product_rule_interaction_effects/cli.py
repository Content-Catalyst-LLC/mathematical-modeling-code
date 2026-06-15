from __future__ import annotations

import argparse
import json
from pathlib import Path

from product_rule_interaction_effects.decomposition import run_default_workflow


def main() -> None:
    parser = argparse.ArgumentParser(description="Product-rule decomposition workflow")
    parser.add_argument("--base-dir", default=".", help="Article folder root")
    args = parser.parse_args()

    summary = run_default_workflow(Path(args.base_dir))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
