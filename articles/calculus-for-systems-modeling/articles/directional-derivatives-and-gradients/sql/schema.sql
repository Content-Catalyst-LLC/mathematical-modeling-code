DROP TABLE IF EXISTS directional_derivative_assumption_registry;
DROP TABLE IF EXISTS directional_derivative_cases;

CREATE TABLE directional_derivative_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO directional_derivative_assumption_registry VALUES
('reference_state','Reference state','Identifies where the gradient and directional derivative are evaluated.','Anchors directional sensitivity to a baseline scenario equilibrium or operating condition.','A directional derivative should not be interpreted without its reference point.'),
('direction_vector','Direction vector','Defines the movement direction through input space.','Connects derivative interpretation to a scenario pathway perturbation or intervention profile.','An undocumented direction makes the derivative uninterpretable.'),
('normalization_rule','Normalization rule','Specifies how the direction vector is converted to a unit vector.','Allows rate comparisons across directions.','Directional derivatives are not comparable if directions are not normalized consistently.'),
('gradient_scale','Gradient scale','Records the units and scaling used for gradient components.','Prevents unit artifacts from being mistaken for meaningful sensitivity.','Gradient direction depends on scaling and the metric used in input space.'),
('feasible_direction','Feasible direction','Checks whether movement respects constraints.','Separates arbitrary mathematical direction from plausible system movement.','The steepest mathematical direction may not be feasible ethical or implementable.');

CREATE TABLE directional_derivative_cases (
    x REAL NOT NULL,
    y REAL NOT NULL,
    direction_x REAL NOT NULL,
    direction_y REAL NOT NULL,
    unit_x REAL NOT NULL,
    unit_y REAL NOT NULL,
    gradient_x REAL NOT NULL,
    gradient_y REAL NOT NULL,
    directional_derivative REAL NOT NULL,
    step_size REAL NOT NULL,
    estimated_change REAL NOT NULL,
    actual_change REAL NOT NULL,
    absolute_error REAL NOT NULL,
    feasible_direction INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO directional_derivative_cases VALUES
(4,3,1,1,0.7071067812,0.7071067812,4.5,4,6.01040764,0.25,1.50260191,1.51822691,0.015625,1,''),
(4,3,2,-1,0.894427191,-0.4472135955,4.5,4,2.2360679775,0.25,0.5590169944,0.5340169944,0.025,1,''),
(8,1,1,1,0.7071067812,0.7071067812,3.5,6,6.717514421,1,6.717514421,6.967514421,0.25,0,'Direction and step move outside the feasible region.');
