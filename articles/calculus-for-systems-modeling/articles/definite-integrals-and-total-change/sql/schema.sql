DROP TABLE IF EXISTS definite_integral_assumption_registry;

CREATE TABLE definite_integral_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO definite_integral_assumption_registry VALUES
('integrand_definition','Integrand definition','The integral accumulates a specified rate, density, intensity, or marginal quantity.','Clarifies what is being accumulated.','If the integrand is misdefined, the total-change estimate is invalid.'),
('interval_bounds','Interval bounds','The lower and upper limits define the accumulation period or domain.','Keeps cumulative claims tied to a specific interval.','Changing bounds changes the result and may change the conclusion.'),
('sign_convention','Sign convention','A definite integral is signed unless the absolute value is integrated.','Distinguishes net change from total activity.','Signed cancellation can hide large offsetting movement.'),
('unit_consistency','Unit consistency','Rate units times integration-variable units should produce accumulated quantity units.','Prevents invalid total-change claims.','Unit mismatch can invalidate the integral interpretation.'),
('numerical_method','Numerical method','Approximate integrals depend on grid, method, and interpolation.','Supports reproducible computational accumulation.','Coarse grids, missing data, or noise can distort total change.');
