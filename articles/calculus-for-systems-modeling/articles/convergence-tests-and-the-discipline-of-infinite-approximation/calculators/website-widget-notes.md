# Website Widget Notes

The `calculator_manifest.json` file is the contract layer for future website integration.

A future website implementation can use this path:

GitHub calculator logic
→ standardized calculator manifest
→ JSON input/output schema
→ PHP or API wrapper
→ front-end calculator interface
→ table/chart/interpretation output

The calculators should remain deterministic, self-contained, and auditable.
