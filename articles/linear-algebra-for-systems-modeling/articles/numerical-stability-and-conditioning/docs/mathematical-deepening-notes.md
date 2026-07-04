# Mathematical Deepening Notes

## Required distinctions

- mathematical exactness versus computed result
- problem conditioning versus algorithmic stability
- residual norm versus forward error
- backward error versus substantive model error
- invertible versus well-conditioned
- small determinant versus singular-value structure
- scaling for computation versus scaling for interpretation
- solver return value versus validated solution
- computed precision versus real-world certainty

## Review checklist

- Report matrix shape, determinant when relevant, condition number, singular value behavior, and rank warning.
- Compute residual norms and relative residuals for each solve or approximation.
- Run perturbation tests to assess sensitivity under small changes in inputs or coefficients.
- Document scaling, units, precision, solver, factorization, pivoting, tolerance, iteration count, and stopping reason.
- Prefer stable algorithms over explicit inverse or normal equations when sensitivity matters.
- Interpret numerical output through finite precision, assumptions, uncertainty, and model purpose.
