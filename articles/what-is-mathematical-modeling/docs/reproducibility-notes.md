# Reproducibility Notes

## Minimum reproducibility standard

A model result should be traceable to:

- article slug;
- code version;
- parameter set;
- scenario definition;
- data source;
- random seed if applicable;
- model assumptions;
- output tables;
- diagnostics;
- run log.

## Terminal workflow

Use:

```bash
make all
```

or run selected targets such as:

```bash
make python
make sql
make haskell
```

## Generated output folders

- `outputs/tables/` for CSV and tabular outputs.
- `outputs/json/` for model cards and diagnostics.
- `outputs/figures/` for plots or graph descriptions.
- `outputs/logs/` for smoke-check logs.
- `outputs/backups/` for non-destructive upgrade backups.
