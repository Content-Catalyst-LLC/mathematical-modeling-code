DROP TABLE IF EXISTS stiffness_review_registry;
DROP TABLE IF EXISTS stiffness_audit_cases;

CREATE TABLE stiffness_review_registry (
    stiffness_key TEXT PRIMARY KEY,
    stiffness_name TEXT NOT NULL,
    numerical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO stiffness_review_registry VALUES
('time_scale_separation','Time-scale separation','Fast and slow processes coexist in the same model.','Explains why a solver may struggle even when the visible trajectory changes slowly.','Time-scale separation should be documented rather than hidden in solver behavior.'),
('explicit_stability_limit','Explicit stability limit','Explicit methods may require small steps to remain stable.','Helps distinguish numerical artifact from system behavior.','An unstable explicit run is not necessarily real system instability.'),
('implicit_method','Implicit method','Uses next-state information and often improves stability for stiff systems.','Supports computation when fast stable dynamics constrain explicit solvers.','Implicit stability does not remove accuracy or interpretation review.'),
('jacobian_review','Jacobian review','Local derivatives reveal coupling and rate separation.','Helps diagnose stiffness in nonlinear systems.','Jacobian conditioning and scaling should be reviewed.'),
('solver_warning','Solver warning','Records step rejection, convergence failure, or stiffness detection.','Provides evidence of computational difficulty.','Warnings should be preserved, not suppressed.'),
('scaling_review','Scaling review','Checks units, nondimensionalization, variable magnitudes, and tolerances.','Helps distinguish real stiffness from poor numerical scaling.','Bad scaling can create avoidable computational difficulty.');

CREATE TABLE stiffness_audit_cases (
    case_id TEXT PRIMARY KEY,
    step_size REAL NOT NULL,
    eigenvalue REAL NOT NULL,
    method TEXT NOT NULL,
    diagnostic_type TEXT NOT NULL,
    interpretation_warning TEXT NOT NULL
);

INSERT INTO stiffness_audit_cases VALUES
('explicit_h_0_1',0.1,-50.0,'explicit_euler','amplification_factor_review','Explicit methods may require very small steps on stiff systems.');
INSERT INTO stiffness_audit_cases VALUES
('implicit_h_0_1',0.1,-50.0,'implicit_euler','amplification_factor_review','Implicit stability does not remove accuracy review.');
INSERT INTO stiffness_audit_cases VALUES
('explicit_h_0_025',0.025,-50.0,'explicit_euler','step_size_refinement','A smaller explicit step may improve stability but increase runtime.');
INSERT INTO stiffness_audit_cases VALUES
('implicit_h_0_025',0.025,-50.0,'implicit_euler','stiff_solver_review','Solver diagnostics should be preserved with stiff simulations.');
