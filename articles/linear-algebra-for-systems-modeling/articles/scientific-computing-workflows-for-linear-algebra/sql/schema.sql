DROP TABLE IF EXISTS scientific_computing_governance_registry;
DROP TABLE IF EXISTS scientific_computing_linear_algebra_audit_cases;

CREATE TABLE scientific_computing_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    computational_role TEXT NOT NULL,
    workflow_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO scientific_computing_governance_registry VALUES
('matrix_construction','Matrix construction','Defines how rows columns values units zeros and missingness become a matrix.','Connects data representation to the mathematical object being computed.','A matrix computation is only as meaningful as the documented construction of the matrix.'),
('representation_choice','Representation choice','Defines dense sparse structured distributed or matrix-free storage.','Controls memory runtime solver choice and interpretive assumptions.','Changing representation can change performance and sometimes interpretation.'),
('numerical_backend','Numerical backend','Defines BLAS LAPACK sparse libraries package versions and hardware behavior.','Controls low-level implementation of high-level matrix operations.','Backend differences can affect performance reproducibility and sometimes numerical results.'),
('solver_configuration','Solver configuration','Defines solver decomposition tolerance precision preconditioner and stopping rule.','Determines how the mathematical problem is computed.','Solver settings should match matrix structure conditioning and modeling purpose.'),
('diagnostic_outputs','Diagnostic outputs','Defines residuals condition numbers convergence histories reconstruction errors and rank checks.','Provides evidence that computed results are numerically reliable.','Final outputs should not be interpreted without diagnostic outputs.'),
('reproducibility_controls','Reproducibility controls','Defines scripts environments package versions random seeds inputs outputs and logs.','Supports rerun audit and revision of scientific-computing workflows.','A workflow that cannot be rerun cannot be fully reviewed.'),
('validation_evidence','Validation evidence','Defines reference cases edge cases domain checks perturbation tests and observed comparisons.','Connects numerical computation to modeled system evidence.','Numerical success is not the same as system validity.'),
('responsible_use','Responsible use','Defines how assumptions uncertainty numerical limits and interpretation boundaries are communicated.','Prevents computed precision from being mistaken for certainty or truth.','Scientific computing outputs should be accompanied by limitations and governance notes.');

CREATE TABLE scientific_computing_linear_algebra_audit_cases (
    model_name TEXT NOT NULL,
    workflow_stage TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    representation TEXT NOT NULL,
    precision TEXT NOT NULL,
    solver_choice TEXT NOT NULL,
    tolerance REAL NOT NULL,
    determinant REAL NOT NULL,
    condition_number_proxy REAL NOT NULL,
    matrix_vector_norm REAL NOT NULL,
    solution_norm REAL NOT NULL,
    residual_norm REAL NOT NULL,
    relative_residual REAL NOT NULL,
    reproducibility_status TEXT NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO scientific_computing_linear_algebra_audit_cases VALUES
('scientific_computing_linear_algebra_audit','matrix_construction_solve_diagnostics_metadata','3x3','dense_sql_registry_demo','double_precision_assumed','direct_small_system_solve',1.0e-10,26.625,3.42,5.82,2.38,0.0,0.0,'pass_residual_tolerance','Scientific computing outputs require matrix construction precision solver tolerance residual conditioning environment validation and assumptions review.');
