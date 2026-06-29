from __future__ import annotations
import csv, json
from pathlib import Path

def main() -> None:
    output_dir = Path("outputs"); output_dir.mkdir(parents=True, exist_ok=True)
    result = {"calculator":"matrix_product_calculator","left_shape":"2x3","right_shape":"3x2","product_shape":"2x2","product_matrix":"1.040000,0.560000;0.585000,0.940000","reverse_product_available":True,"warning":"Matrix products require order, intermediate-layer meaning, units, row-column alignment, and pathway validity review."}
    (output_dir/"matrix_product_calculator.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    with (output_dir/"matrix_product_calculator.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.keys())); writer.writeheader(); writer.writerow(result)
    print(json.dumps(result, indent=2, sort_keys=True))
if __name__ == "__main__": main()
