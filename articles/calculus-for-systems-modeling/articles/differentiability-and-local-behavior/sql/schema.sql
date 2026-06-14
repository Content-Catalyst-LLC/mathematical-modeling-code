DROP TABLE IF EXISTS differentiability_assumption_registry;
DROP TABLE IF EXISTS derivative_diagnostic_threshold;
DROP TABLE IF EXISTS nonsmooth_case_type;

CREATE TABLE differentiability_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    concept_name TEXT NOT NULL,
    formal_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

CREATE TABLE derivative_diagnostic_threshold (
    threshold_key TEXT PRIMARY KEY,
    threshold_value REAL NOT NULL CHECK (threshold_value >= 0),
    interpretation TEXT NOT NULL
);

CREATE TABLE nonsmooth_case_type (
    case_key TEXT PRIMARY KEY,
    case_name TEXT NOT NULL,
    diagnostic_signal TEXT NOT NULL,
    modeling_warning TEXT NOT NULL
);

INSERT INTO differentiability_assumption_registry VALUES
('ordinary_derivative','Ordinary derivative','Defines a stable limiting rate of change at a point.','Supports marginal analysis and local sensitivity in one-dimensional models.','Requires the difference quotient to converge from both sides.'),
('local_linearization','Local linearization','Represents differentiability as first-order approximation with small remainder.','Supports perturbation analysis, calibration, and local response estimates.','Only valid near the operating point and inside the model domain.'),
('jacobian','Jacobian matrix','Represents the derivative of a vector-valued function as a linear map.','Supports local stability, parameter sensitivity, and Newton-type methods.','May be undefined or misleading near thresholds, kinks, or discontinuities.'),
('frechet_derivative','Fréchet derivative','Defines differentiability as a bounded linear approximation in normed spaces.','Supports advanced function-space and trajectory-based models.','Stronger than directional sensitivity and requires uniform small-remainder control.'),
('nonsmooth_model','Nonsmooth model','Identifies cases where ordinary derivatives fail or are one-sided.','Supports piecewise, threshold, and constrained systems modeling.','Requires one-sided derivatives, subgradients, event logic, or generalized tools.');

INSERT INTO derivative_diagnostic_threshold VALUES
('one_sided_gap',0.5,'Forward/backward finite-difference disagreement above this value is flagged.'),
('relative_linearization_error',0.1,'Large local-linearization error relative to perturbation is flagged.');

INSERT INTO nonsmooth_case_type VALUES
('kink','Kink','Forward and backward derivatives disagree.','Use one-sided derivatives, subgradients, or piecewise analysis.'),
('boundary','Boundary derivative','Only one side of the perturbation is feasible.','Use domain-relative or one-sided derivative logic.'),
('threshold','Threshold rule','Local formula changes when an active rule changes.','Do not apply a single derivative across the threshold.'),
('max_min','Max/min nonsmoothness','Active branch changes.','Use nonsmooth optimization or branch-wise derivatives.');
