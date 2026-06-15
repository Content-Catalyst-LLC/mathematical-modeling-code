DROP TABLE IF EXISTS second_derivative_assumption_registry;

CREATE TABLE second_derivative_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO second_derivative_assumption_registry VALUES
('twice_differentiability','Twice differentiability','A second derivative requires the first derivative to be differentiable.','Supports acceleration, concavity, and curvature interpretation.','Nonsmooth systems may not support second-derivative claims.'),
('operating_point','Operating point','Second derivatives are evaluated locally.','Keeps acceleration and curvature claims state-specific.','Curvature may change across regimes or thresholds.'),
('concavity_sign','Concavity sign','The sign of the second derivative indicates local bending.','Supports interpretation of increasing or diminishing marginal effects.','A zero second derivative at a point does not alone prove inflection.'),
('finite_difference_step','Finite-difference step size','Numerical second derivatives depend on local difference formulas.','Supports reproducible curvature and acceleration estimation.','Step sizes that are too large or too small can distort estimates.'),
('noise_sensitivity','Noise sensitivity','Second derivatives amplify measurement noise.','Warns against overinterpreting acceleration in noisy data.','Smoothing and uncertainty assumptions must be documented.');
