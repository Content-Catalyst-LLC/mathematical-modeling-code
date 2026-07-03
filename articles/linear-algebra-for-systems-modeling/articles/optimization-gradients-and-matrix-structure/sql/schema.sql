DROP TABLE IF EXISTS optimization_governance_registry;
DROP TABLE IF EXISTS optimization_matrix_audit_cases;

CREATE TABLE optimization_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO optimization_governance_registry VALUES
('decision_variables','Decision variables','Define the vector of quantities the model is allowed to choose.','Determine what actions allocations parameters or flows are controllable.','If variables do not match real decision authority the optimized solution may be unusable.'),
('objective_function','Objective function','Defines what the model minimizes or maximizes.','Determines what the model treats as success.','An objective may be a proxy that excludes important system values or harms.'),
('constraint_matrix','Constraint matrix','Encodes equality inequality balance capacity or feasibility relationships.','Defines the feasible region of system decisions.','Missing constraints can make an optimized decision infeasible or harmful.'),
('gradient_formula','Gradient formula','Defines local sensitivity and update direction.','Guides iterative search through parameter or decision space.','Incorrect gradients or poor scaling can invalidate optimization behavior.'),
('curvature_diagnostics','Curvature diagnostics','Use Hessians eigenvalues or singular values to assess objective shape.','Explain convergence uniqueness convexity and sensitivity.','Curvature should be reviewed before trusting solver behavior.'),
('conditioning','Conditioning','Measures numerical sensitivity of matrices or solution systems.','Determines whether optimized results are stable under perturbation.','High condition numbers require sensitivity testing and cautious interpretation.'),
('regularization','Regularization','Adds penalties or constraints to stabilize or structure solutions.','Expresses a preference for smaller smoother sparse or lower-rank solutions.','Regularization strength is a modeling choice and should be validated.'),
('responsible_use','Responsible use','Defines how objectives constraints sensitivity uncertainty and limits are communicated.','Prevents optimized results from being overstated as complete system answers.','An optimum is a model result under assumptions not automatic policy causality or truth.');

CREATE TABLE optimization_matrix_audit_cases (
    model_name TEXT NOT NULL,
    observations INTEGER NOT NULL,
    features INTEGER NOT NULL,
    objective TEXT NOT NULL,
    solver TEXT NOT NULL,
    regularization_strength REAL NOT NULL,
    feature_matrix_condition_number REAL NOT NULL,
    hessian_condition_number REAL NOT NULL,
    gradient_norm_final REAL NOT NULL,
    objective_initial REAL NOT NULL,
    objective_final REAL NOT NULL,
    closed_form_gap_norm REAL NOT NULL,
    training_rmse REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO optimization_matrix_audit_cases VALUES
('synthetic_optimization_gradient_matrix_audit',10,5,'mean_squared_error_plus_l2_regularization','fixed_step_gradient_descent_compared_with_closed_form_ridge_solution',0.75,18.4,3.8,0.0009,52.0,4.3,0.002,1.9,'An optimum is a model result under assumptions not automatic policy causality or truth.');
