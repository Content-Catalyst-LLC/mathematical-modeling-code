DROP TABLE IF EXISTS derivative_rate_assumption_registry;
DROP TABLE IF EXISTS derivative_method_registry;
DROP TABLE IF EXISTS derivative_warning_registry;

CREATE TABLE derivative_rate_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    formal_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

CREATE TABLE derivative_method_registry (
    method_key TEXT PRIMARY KEY,
    method_name TEXT NOT NULL,
    approximation_role TEXT NOT NULL,
    numerical_warning TEXT NOT NULL
);

CREATE TABLE derivative_warning_registry (
    warning_key TEXT PRIMARY KEY,
    warning_name TEXT NOT NULL,
    interpretation TEXT NOT NULL
);

INSERT INTO derivative_rate_assumption_registry VALUES
('average_rate','Average rate of change','Measures finite output change over finite input interval.','Useful for observed data intervals and coarse-scale model summaries.','May conceal local thresholds, shocks, or nonlinear behavior inside the interval.'),
('instantaneous_rate','Instantaneous rate of change','Defined as the limit of average rates as interval length approaches zero.','Supports local sensitivity, velocity, marginal analysis, and dynamic interpretation.','Requires differentiability at the operating point.'),
('relative_rate','Relative rate and elasticity','Scales derivative by output or by input-output ratio.','Supports proportional sensitivity and dimensionless comparison.','Can be unstable near zero values or outside positive domains.'),
('vector_field','State-space rate vector','Defines system motion as a derivative of state with respect to time.','Supports differential equation modeling, simulation, and local stability analysis.','Requires invariant-domain checks and careful numerical discretization.');

INSERT INTO derivative_method_registry VALUES
('forward_difference','Forward difference','One-sided finite derivative estimate.','First-order truncation error and boundary sensitivity.'),
('backward_difference','Backward difference','One-sided finite derivative estimate from the left.','First-order truncation error and boundary sensitivity.'),
('central_difference','Central difference','Symmetric finite derivative estimate.','Usually second-order for smooth functions but invalid across discontinuities or boundaries.'),
('automatic_differentiation','Automatic differentiation','Computes exact derivative of implemented program under differentiable operations.','Derivative of code may not equal derivative of the intended real-world system.');

INSERT INTO derivative_warning_registry VALUES
('units','Units required','A derivative must state output units per input unit.'),
('locality','Local validity','A derivative is local and should not be used as a global claim without further argument.'),
('thresholds','Threshold warning','Derivatives may fail or change across kinks, thresholds, and structural breaks.'),
('finite_precision','Finite precision','Numerical derivatives require step-size and roundoff review.');
