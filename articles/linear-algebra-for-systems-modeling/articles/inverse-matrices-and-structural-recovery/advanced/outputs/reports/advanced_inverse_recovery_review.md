# Advanced Inverse Recovery Review

- **square_matrix_check** (required): Ordinary inverse claims require square matrices.
- **invertibility_check** (required): Record determinant, rank, pivots, and nullity before recovery claims.
- **residual_check** (required): Report residuals after recovered values are computed.
- **conditioning_review** (required): Assess whether recovery is numerically stable.
- **solver_choice_review** (required): Prefer solving systems directly over forming explicit inverses for numerical workflows.
- **pseudoinverse_boundary** (recommended): Use pseudoinverse language for rectangular, rank-deficient, or approximate recovery.
