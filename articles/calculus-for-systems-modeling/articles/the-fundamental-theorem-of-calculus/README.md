# The Fundamental Theorem of Calculus

Companion code and reproducible workflows for **The Fundamental Theorem of Calculus** in the **Calculus for Systems Modeling** series.

## Themes

- FTC Part I: differentiating accumulation functions;
- FTC Part II: evaluating definite integrals through endpoint differences;
- local rates and accumulated change;
- state trajectories and flow laws;
- baseline values and constants;
- signed accumulation and net change;
- unit consistency;
- rate-state reconciliation;
- numerical residual diagnostics;
- generated Markdown/JSON audit reports.

## Run

```bash
make smoke
make advanced
make all
```

## Principle

If a model asserts \(Q'(t)=r(t)\), then accumulated rate and endpoint difference should reconcile within documented numerical, measurement, and modeling tolerance.
