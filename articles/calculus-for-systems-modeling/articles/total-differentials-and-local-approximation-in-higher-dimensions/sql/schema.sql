DROP TABLE IF EXISTS total_differential_assumption_registry;
DROP TABLE IF EXISTS total_differential_cases;

CREATE TABLE total_differential_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO total_differential_assumption_registry VALUES
('reference_state','Reference state','Identifies where the total differential is evaluated.','Anchors the local approximation to a baseline scenario equilibrium or operating condition.','A differential estimate should not be interpreted without its reference point.'),
('partial_derivatives','Partial derivatives','Provide local sensitivities used in the differential estimate.','Show how each input contributes to output change near the reference state.','Partial derivatives may change across the input space.'),
('displacement_vector','Displacement vector','Records the small input changes being evaluated.','Defines the modeled movement from the reference state.','A differential estimate is meaningful only for the stated displacement.'),
('feasible_movement','Feasible movement','Checks whether the displacement respects constraints.','Separates mathematical movement from plausible system movement.','An infeasible displacement should not be treated as a practical scenario.'),
('local_validity','Local validity','Defines where the first-order approximation is intended to hold.','Prevents tangent-plane reasoning from becoming global model interpretation.','Large perturbations thresholds and nonlinear curvature can invalidate the approximation.');

CREATE TABLE total_differential_cases (
    x REAL NOT NULL,
    y REAL NOT NULL,
    dx REAL NOT NULL,
    dy REAL NOT NULL,
    baseline_output REAL NOT NULL,
    actual_output REAL NOT NULL,
    actual_change REAL NOT NULL,
    differential_estimate REAL NOT NULL,
    absolute_error REAL NOT NULL,
    feasible_displacement INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO total_differential_cases VALUES
(4,3,0.2,-0.1,28,28.49,0.49,0.5,0.01,1,''),
(4,3,1,1,28,36.5,8.5,8.5,0,1,''),
(8,1,1,1,46,57.5,11.5,10.5,1,0,'Displacement is outside the feasible region.');
