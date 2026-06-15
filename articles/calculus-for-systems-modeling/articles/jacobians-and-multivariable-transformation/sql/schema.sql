DROP TABLE IF EXISTS jacobian_assumption_registry;
DROP TABLE IF EXISTS jacobian_cases;

CREATE TABLE jacobian_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO jacobian_assumption_registry VALUES
('reference_state','Reference state','Identifies where the Jacobian is evaluated.','Anchors local transformation to a baseline scenario equilibrium or calibration point.','A Jacobian should not be interpreted without its reference state.'),
('input_output_definitions','Input and output definitions','Clarifies the dimensions units and components of the transformation.','Prevents matrix entries from being treated as context-free numbers.','Rows and columns are uninterpretable without documented variables.'),
('local_linearization','Local linearization','Uses the Jacobian to approximate nearby output movement.','Supports perturbation analysis sensitivity review and numerical methods.','Large movements may require nonlinear analysis.'),
('determinant_scaling','Determinant scaling','Measures local area or volume scaling for square transformations.','Supports coordinate transformations integration and density changes.','Singular or near-singular determinants require caution.'),
('conditioning','Conditioning','Assesses whether the transformation amplifies error.','Flags unstable inverse problems fragile calibration and high sensitivity.','Ill-conditioned Jacobians can make conclusions numerically fragile.');

CREATE TABLE jacobian_cases (
    x REAL NOT NULL,
    y REAL NOT NULL,
    dx REAL NOT NULL,
    dy REAL NOT NULL,
    j11 REAL NOT NULL,
    j12 REAL NOT NULL,
    j21 REAL NOT NULL,
    j22 REAL NOT NULL,
    determinant REAL NOT NULL,
    approximate_change_1 REAL NOT NULL,
    approximate_change_2 REAL NOT NULL,
    actual_change_1 REAL NOT NULL,
    actual_change_2 REAL NOT NULL,
    error_norm REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO jacobian_cases VALUES
(2,1,0.1,-0.05,4,1,1,5,19,0.35,-0.15,0.36,-0.155,0.0111803399,''),
(2,1,0.5,0.5,4,1,1,5,19,2.5,3.0,2.75,3.25,0.3535533906,''),
(0,0,0.1,0.1,0,1,0,3,0,0.1,0.3,0.11,0.31,0.0141421356,'Jacobian is singular or near singular.');
