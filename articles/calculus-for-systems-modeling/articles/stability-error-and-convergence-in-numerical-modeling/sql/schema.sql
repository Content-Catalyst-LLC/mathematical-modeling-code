DROP TABLE IF EXISTS numerical_reliability_registry;
DROP TABLE IF EXISTS convergence_audit_cases;

CREATE TABLE numerical_reliability_registry (
    reliability_key TEXT PRIMARY KEY,
    reliability_name TEXT NOT NULL,
    numerical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO numerical_reliability_registry VALUES
('local_error','Local error','Error introduced by one numerical step.','Helps evaluate step-level approximation quality.','Small local error can still accumulate into important global error.'),
('global_error','Global error','Accumulated error across the simulation horizon.','Shapes interpretation of trajectories, endpoints, and thresholds.','Global error often matters more than a single-step estimate.'),
('stability','Numerical stability','Controls whether numerical perturbations grow or remain bounded.','Helps distinguish solver artifact from system behavior.','Unstable methods can create artificial oscillation or blow-up.'),
('convergence','Convergence','Checks whether outputs approach a stable result under refinement.','Supports confidence that the numerical method is approximating the intended model.','Convergence is not empirical validation.'),
('roundoff','Round-off error','Error from finite-precision arithmetic.','Can matter in long simulations, ill-conditioned systems, or extreme scaling.','Smaller step sizes do not always improve results indefinitely.'),
('diagnostics','Solver diagnostics','Record warnings, residuals, step behavior, and constraint checks.','Supports reproducible review of numerical reliability.','A completed solver run is not automatically a trustworthy result.');

CREATE TABLE convergence_audit_cases (
    case_id TEXT PRIMARY KEY,
    solver_method TEXT NOT NULL,
    step_size REAL NOT NULL,
    diagnostic_type TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO convergence_audit_cases VALUES
('rk4_h_1','fixed_step_rk4',1.0,'step_size_refinement','Coarse numerical outputs should not be treated as verified.');
INSERT INTO convergence_audit_cases VALUES
('rk4_h_0_5','fixed_step_rk4',0.5,'step_size_refinement','Refinement tests numerical behavior, not empirical validity.');
INSERT INTO convergence_audit_cases VALUES
('rk4_h_0_25','fixed_step_rk4',0.25,'convergence_review','Convergence should be documented with assumptions and solver settings.');
INSERT INTO convergence_audit_cases VALUES
('rk4_h_0_125','fixed_step_rk4',0.125,'diagnostic_review','Numerical confidence remains separate from model validity.');
