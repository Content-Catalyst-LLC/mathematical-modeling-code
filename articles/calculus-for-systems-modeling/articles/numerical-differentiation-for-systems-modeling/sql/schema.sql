DROP TABLE IF EXISTS numerical_differentiation_assumption_registry;
DROP TABLE IF EXISTS numerical_differentiation_audit_cases;

CREATE TABLE numerical_differentiation_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO numerical_differentiation_assumption_registry VALUES
('difference_formula','Difference formula','Defines how nearby values estimate a derivative.','Controls whether the estimate is forward, backward, central, or higher-order.','The formula should be documented, especially near boundaries.'),
('step_size','Step size','Defines spacing between sampled values or perturbations.','Controls the balance between truncation error, roundoff error, and data noise.','Step-size sensitivity should be tested.'),
('boundary_handling','Boundary handling','Defines derivative estimates at the beginning, end, or edge of data.','Controls interpretation near time-series endpoints or spatial boundaries.','Boundary derivatives are often less reliable than interior derivatives.'),
('noise_treatment','Noise treatment','Defines smoothing, filtering, interpolation, or statistical estimation.','Prevents derivative estimates from amplifying measurement noise unchecked.','Smoothing choices should be justified and not used to hide uncertainty.'),
('validation_benchmark','Validation benchmark','Compares derivative estimates against known or simulated truth when available.','Helps identify formula, step-size, or implementation errors.','Synthetic benchmarks do not guarantee empirical validity.'),
('interpretation_scope','Interpretation scope','Defines whether derivative estimates are exploratory, diagnostic, or decision-supporting.','Clarifies how strongly rate estimates should be used in conclusions.','Derivative estimates should not be overstated when data quality is weak.');

CREATE TABLE numerical_differentiation_audit_cases (
    scenario TEXT NOT NULL,
    start_value REAL NOT NULL,
    stop_value REAL NOT NULL,
    step_size REAL NOT NULL,
    formula_family TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO numerical_differentiation_audit_cases VALUES
('smooth_synthetic_signal_benchmark',0.0,10.0,0.1,'forward_backward_central','Numerical derivatives depend on step size, formula choice, boundary handling, smoothness, and noise.');
