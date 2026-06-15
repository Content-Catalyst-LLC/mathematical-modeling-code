from __future__ import annotations
import argparse, csv, json
from dataclasses import asdict, dataclass
from pathlib import Path
@dataclass(frozen=True)
class CanvasCard:
    card_id: str; title: str; category: str; score: int; status: str; review_date: str; governance_note: str
cards=[
 CanvasCard('separability','Separability','model structure',96,'active','2026-06-15','Rate law must factor into independent-variable and state-variable components.'),
 CanvasCard('state-domain','State Domain','assumption',95,'active','2026-06-15','Excluded states and domain restrictions should be documented.'),
 CanvasCard('initial-condition','Initial Condition','assumption',94,'active','2026-06-15','Initial states select specific trajectories.'),
 CanvasCard('simple-dynamic-law','Simple Dynamic Law','model structure',93,'review','2026-06-15','Simple laws clarify mechanism but can hide interactions and changing capacity.'),
 CanvasCard('solver-comparison','Solver Comparison','computation',92,'review','2026-06-15','Analytical and Euler solutions should be compared under step-size review.')]
def main():
    p=argparse.ArgumentParser(); p.add_argument('--output-dir', type=Path, default=Path('outputs')); args=p.parse_args(); out=args.output_dir
    (out/'json').mkdir(parents=True, exist_ok=True); (out/'tables').mkdir(parents=True, exist_ok=True); (out/'reports').mkdir(parents=True, exist_ok=True)
    rows=[asdict(c) for c in cards]; (out/'json'/'canvas_cards.json').write_text(json.dumps(rows, indent=2, sort_keys=True), encoding='utf-8')
    with (out/'tables'/'canvas_cards.csv').open('w', newline='', encoding='utf-8') as h:
        w=csv.DictWriter(h, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    (out/'reports'/'canvas_governance_queue.md').write_text('# Catalyst Canvas Governance Queue\n\n'+'\n'.join(f"- **{c.title}** ({c.status}, score {c.score}): {c.governance_note}" for c in cards)+'\n', encoding='utf-8')
    print('Catalyst Canvas cards and governance queue generated.')
if __name__ == '__main__': main()
