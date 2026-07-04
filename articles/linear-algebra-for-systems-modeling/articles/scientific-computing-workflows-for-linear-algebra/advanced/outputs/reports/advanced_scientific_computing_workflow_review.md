# Advanced Scientific Computing Workflow Review

- **matrix_construction** (required): Document rows, columns, values, units, zeros, missingness, data source, and construction assumptions.
- **representation_choice** (required): Choose dense, sparse, structured, distributed, or matrix-free representation based on matrix structure and system scale.
- **numerical_backend** (required): Record BLAS, LAPACK, sparse libraries, package versions, hardware, threading, and language bindings.
- **solver_configuration** (required): Document solver, factorization, tolerance, precision, preconditioner, iteration count, and stopping reason.
- **diagnostic_outputs** (required): Save residuals, condition estimates, convergence histories, reconstruction errors, rank checks, and performance diagnostics.
- **reproducibility_controls** (required): Preserve scripts, environments, package versions, random seeds, inputs, outputs, logs, and generated reports.
- **validation_evidence** (required): Use reference cases, edge cases, domain checks, perturbation tests, and observed comparisons.
- **responsible_use** (required): Communicate assumptions, uncertainty, numerical limits, performance constraints, and interpretation boundaries.
