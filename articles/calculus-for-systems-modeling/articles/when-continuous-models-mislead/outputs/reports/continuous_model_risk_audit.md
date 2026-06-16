# Continuous Model Risk Audit

## Continuity Assumptions
- **smooth_state_change** (state trajectory x(t)): state changes gradually over modeled time. Review: Are shocks, events, or thresholds possible?. Smooth output does not prove smooth system behavior.
- **continuous_rate_function** (dx/dt = f(x,t,theta)): rate can be represented as a continuous function. Review: Does the process change through discrete decisions or regime switches?. Rate continuity should be justified at the modeled scale.
- **aggregate_representative_variable** (mean state or average exposure): aggregate variable represents the system adequately. Review: Does heterogeneity matter for the claim?. Averages can hide local stress, inequality, or bottlenecks.

## Misleading Continuity Risks
- **false_smoothness**: smooth curve hides structural breaks. Consequence: threshold, failure, or event dynamics are missed. Response: test for breaks and document discontinuities.
- **equilibrium_bias**: steady-state result is overinterpreted. Consequence: transition cost, overshoot, delay, or distributional effect is hidden. Response: analyze trajectories and stability, not only equilibria.
- **solver_confidence**: successful computation is mistaken for validation. Consequence: numerical artifacts appear as model insight. Response: record solver method, tolerance, convergence, and warnings.
- **aggregation_risk**: average hides heterogeneity. Consequence: local stress, inequality, or bottlenecks are hidden. Response: inspect distributions and subgroups.
- **domain_drift**: local model is extrapolated beyond its domain. Consequence: smooth projection exceeds evidence. Response: define scope and update triggers.

## Solver Diagnostics
- **step_size_check**: tests whether results change under smaller time steps. Required record: time step, method, output difference. Large time steps can miss fast dynamics or threshold crossing.
- **stiffness_check**: flags fast and slow dynamics that challenge numerical methods. Required record: solver type, stiffness warning, rejected steps. Stiff systems require solver-specific diagnostics.
- **convergence_check**: records whether numerical solution converged. Required record: convergence flag, tolerance, iteration count. A plotted output can hide convergence failure.

Continuous models are approximations whose smooth assumptions, solver settings, and claim boundaries must be reviewed.
