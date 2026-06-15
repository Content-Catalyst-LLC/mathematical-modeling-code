DROP TABLE IF EXISTS partial_derivative_assumption_registry;
DROP TABLE IF EXISTS partial_derivative_cases;

CREATE TABLE partial_derivative_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO partial_derivative_assumption_registry VALUES
('reference_state','Reference state','Identifies where the partial derivative is evaluated.','Anchors sensitivity to a baseline scenario equilibrium or operating condition.','A partial derivative should not be interpreted without its evaluation point.'),
('fixed_variables','Fixed variables','Identifies which variables are held constant during differentiation.','Clarifies the ceteris paribus comparison being made.','Holding variables fixed may be infeasible in coupled systems.'),
('interaction_structure','Interaction structure','Records whether one input changes the effect of another.','Connects partial derivatives to combined system behavior.','Omitted interactions may distort local sensitivity interpretation.'),
('cross_partial','Cross partial','Measures how one partial derivative changes with another variable.','Helps identify complementarity substitution reinforcement or damping.','Cross-partial interpretation depends on units smoothness and model structure.'),
('feasible_change','Feasible change','Distinguishes coordinate change from allowed movement under constraints.','Prevents mathematical sensitivity from being treated as practical intervention effect.','A large partial derivative may not imply feasible leverage.');

CREATE TABLE partial_derivative_cases (
    x REAL NOT NULL,
    y REAL NOT NULL,
    output REAL NOT NULL,
    partial_x REAL NOT NULL,
    partial_y REAL NOT NULL,
    cross_partial_xy REAL NOT NULL,
    feasible INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO partial_derivative_cases VALUES
(2,4,18,5,3,0.5,1,''),
(8,4,48,5,6,0.5,0,'Input combination is outside the feasible region.'),
(6,3,33,4.5,5,0.5,1,'');
