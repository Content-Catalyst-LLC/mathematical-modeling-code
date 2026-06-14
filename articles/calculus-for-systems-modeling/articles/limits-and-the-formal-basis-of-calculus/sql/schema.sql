DROP TABLE IF EXISTS limit_assumption_registry;
DROP TABLE IF EXISTS epsilon_band;
DROP TABLE IF EXISTS convergence_mode;

CREATE TABLE limit_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    formal_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

CREATE TABLE epsilon_band (
    epsilon_key TEXT PRIMARY KEY,
    epsilon_value REAL NOT NULL CHECK (epsilon_value > 0),
    interpretation TEXT NOT NULL
);

CREATE TABLE convergence_mode (
    mode_key TEXT PRIMARY KEY,
    mode_name TEXT NOT NULL,
    mathematical_strength TEXT NOT NULL,
    modeling_warning TEXT NOT NULL
);

INSERT INTO limit_assumption_registry VALUES
('epsilon_delta','Epsilon-delta limit','Defines local convergence through quantified tolerances.','Clarifies what it means for model outputs to approach a target under input refinement.','Requires an admissible domain and a specified output metric.'),
('sequential_limit','Sequential characterization','Tests limits through all admissible sequences approaching the target.','Useful for identifying path-dependent or sequence-dependent model behavior.','A single sequence is not enough to prove a limit, but two conflicting sequences can disprove one.'),
('uniform_convergence','Uniform convergence','Controls convergence across an entire domain using a supremum norm.','Supports stronger claims about global approximation behavior.','Pointwise convergence alone may not preserve continuity or stability.'),
('interchange_limits','Interchange of limits and operations','Concerns when limits commute with integration, differentiation, expectation, or optimization.','Important for simulation, aggregation, uncertainty, and sensitivity analysis.','Requires additional hypotheses such as domination, uniform convergence, compactness, or stability.');

INSERT INTO epsilon_band VALUES
('coarse',0.1,'Coarse tolerance for exploratory checks.'),
('moderate',0.01,'Moderate tolerance for computational review.'),
('fine',0.001,'Fine tolerance for convergence review.'),
('strict',0.0001,'Strict tolerance; review roundoff and method assumptions.');

INSERT INTO convergence_mode VALUES
('pointwise','Pointwise convergence','Weak for global preservation.','May fail to preserve continuity or stability.'),
('uniform','Uniform convergence','Stronger global control over a domain.','Requires domain-wide error control, not only sampled checks.'),
('norm','Norm convergence','Depends on chosen function-space norm.','Interpretation changes with norm selection.'),
('weak','Weak convergence','Often used in probability and functional analysis.','May not control pointwise behavior or strong error.');
