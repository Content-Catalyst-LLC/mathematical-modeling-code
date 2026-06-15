DROP TABLE IF EXISTS hessian_assumption_registry;
DROP TABLE IF EXISTS hessian_cases;

CREATE TABLE hessian_assumption_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO hessian_assumption_registry VALUES
('reference_state','Reference state','Identifies where the Hessian is evaluated.','Anchors curvature analysis to a baseline critical point scenario or calibration region.','A Hessian should not be interpreted without its reference state.'),
('second_order_derivatives','Second-order derivatives','Record how first-order sensitivities change with input movement.','Reveal curvature acceleration and changing marginal response.','Second derivatives are local and depend on smoothness assumptions.'),
('cross_partials','Cross partials','Measure how sensitivity to one variable changes as another variable changes.','Support interaction review in multivariable systems.','Interaction structure should not be treated as causal without model justification.'),
('definiteness','Definiteness','Classifies local curvature using Hessian signs determinants or eigenvalues.','Helps distinguish minima maxima saddle points and inconclusive regions.','Local classification does not imply global optimality.'),
('conditioning','Conditioning','Assesses curvature spread and numerical fragility.','Flags weak identification narrow valleys and unstable optimization.','Conditioning depends on scaling units and parameterization.');

CREATE TABLE hessian_cases (
    x REAL NOT NULL,
    y REAL NOT NULL,
    dx REAL NOT NULL,
    dy REAL NOT NULL,
    gradient_x REAL NOT NULL,
    gradient_y REAL NOT NULL,
    h11 REAL NOT NULL,
    h12 REAL NOT NULL,
    h21 REAL NOT NULL,
    h22 REAL NOT NULL,
    determinant REAL NOT NULL,
    trace REAL NOT NULL,
    classification TEXT NOT NULL,
    first_order_change REAL NOT NULL,
    second_order_change REAL NOT NULL,
    actual_change REAL NOT NULL,
    first_order_error REAL NOT NULL,
    second_order_error REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO hessian_cases VALUES
(2,1,0.1,-0.05,5.8,8.8,2.4,1.8,1.8,6,11.16,8.4,'positive definite',0.14,0.147,0.1475,0.0075,0.0005,''),
(2,1,0.5,0.5,5.8,8.8,2.4,1.8,1.8,6,11.16,8.4,'positive definite',7.3,8.8,8.85,1.55,0.05,''),
(-5,0,0.2,0.1,-10,0,2,-1,-1,6,11,8,'positive definite',-2, -1.95, -1.948, 0.052, 0.002,'');
