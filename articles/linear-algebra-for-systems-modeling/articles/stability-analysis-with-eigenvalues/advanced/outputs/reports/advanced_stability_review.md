# Advanced Stability Analysis Review

- **time_model** (required): State whether the matrix is a discrete-time update, continuous-time generator, or local Jacobian.
- **stability_threshold** (required): Use unit-circle tests for discrete time and real-part tests for continuous time.
- **reference_state** (required): Define the equilibrium, baseline, trajectory, distribution, or operating region being evaluated.
- **spectral_gap** (recommended): Review whether stable, unstable, and dominant modes are well separated.
- **nonnormality** (recommended): Check whether transient growth could matter despite asymptotic decay.
- **domain_accountability** (required): Explain what stability means for the domain; stable does not automatically mean desirable.
