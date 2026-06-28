DROP TABLE IF EXISTS linear_transformation_assumption_registry;
DROP TABLE IF EXISTS linear_transformation_behavior_audit_cases;

CREATE TABLE linear_transformation_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO linear_transformation_assumption_registry VALUES
('linear_transformation','Linear transformation','A map preserving addition and scalar multiplication.','Represents a structured input-output behavior rule.','Linearity should be justified for the modeled range and purpose.'),
('matrix_action','Matrix action','The product A times x transforms an input vector into an output vector.','Shows modeled system response to a specific state.','Output interpretation depends on row meanings column meanings and units.'),
('image','Image','The set of all reachable outputs of the transformation.','Shows what behaviors the model can produce.','The codomain may include outputs the model cannot actually reach.'),
('kernel','Kernel','The set of inputs mapped to zero.','Shows invisible input directions or collapsed variation.','A nontrivial kernel prevents unique recovery.'),
('basis_behavior','Basis behavior','The columns of a matrix show transformed basis vectors.','Shows how each input direction contributes to system response.','Basis-dependent interpretation should be documented.'),
('amplification','Amplification','The transformation may increase the norm of state differences.','Small input uncertainty can become larger output uncertainty.','Sensitivity and conditioning should be reviewed before decision use.');

CREATE TABLE linear_transformation_behavior_audit_cases (
    system_name TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    column_count INTEGER NOT NULL,
    input_state TEXT NOT NULL,
    output_state TEXT NOT NULL,
    rank INTEGER NOT NULL,
    nullity INTEGER NOT NULL,
    input_norm REAL NOT NULL,
    output_norm REAL NOT NULL,
    amplification_ratio REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO linear_transformation_behavior_audit_cases VALUES
('three_component_system_response',3,3,'100.000000,60.000000,30.000000','126.000000,75.500000,42.000000',3,0,120.415946,152.750205,1.268531,'Matrix action requires row meanings column meanings units scaling and sensitivity review.');
