DROP TABLE IF EXISTS sensitivity_assumption_registry;

CREATE TABLE sensitivity_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO sensitivity_assumption_registry VALUES
('baseline_operating_point','Baseline operating point','Derivative-based sensitivity is local to a point or parameter value.','Keeps marginal response tied to a specific system condition.','Do not generalize local sensitivity across the whole domain without evidence.'),
('nonzero_normalization','Nonzero normalization','Elasticity requires nonzero input and output for proportional interpretation.','Prevents undefined relative-change calculations.','Elasticity is unreliable or undefined near zero.'),
('positive_log_domain','Positive log domain','Log-derivative interpretation requires positive input and output.','Supports proportional-change interpretation.','Negative or sign-changing quantities require special handling.'),
('step_size_choice','Finite-difference step size','Numerical derivatives depend on perturbation size.','Supports reproducible sensitivity estimation.','Step sizes that are too large or too small can distort the result.'),
('parameter_range','Parameter range','Sensitivity depends on the range of values examined.','Supports robustness and scenario interpretation.','A narrow range may hide nonlinear or threshold behavior.');
