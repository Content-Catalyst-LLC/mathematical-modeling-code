DROP TABLE IF EXISTS decomposition_governance_registry;
DROP TABLE IF EXISTS decomposition_workflow_audit_cases;

CREATE TABLE decomposition_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    workflow_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO decomposition_governance_registry VALUES
('matrix_structure','Matrix structure','Defines shape symmetry sparsity rank scaling and definiteness before factorization.','Determines which decomposition is mathematically and computationally appropriate.','Decomposition should not be chosen before matrix structure is reviewed.'),
('decomposition_choice','Decomposition choice','Defines LU QR Cholesky eigen Schur SVD sparse factorization or low-rank workflow.','Connects modeling purpose to numerical method.','Different decompositions reveal different structures and carry different risks.'),
('pivoting_and_ordering','Pivoting and ordering','Defines row or column permutations used to improve stability or sparsity.','Controls numerical behavior fill-in and reproducibility.','Permutation choices should be recorded when they affect factors or interpretation.'),
('rank_tolerance','Rank tolerance','Defines the threshold used to distinguish signal dependence and near-zero structure.','Controls rank estimates pseudoinverses and low-rank approximations.','Rank is tolerance-dependent in numerical workflows.'),
('reconstruction_error','Reconstruction error','Measures how well factors reproduce the original matrix or approximation.','Validates factorization quality and low-rank loss.','A decomposition should be checked against reconstruction or residual diagnostics.'),
('conditioning','Conditioning','Measures sensitivity of the matrix problem to perturbation.','Determines whether decomposition results are numerically reliable.','Ill-conditioned matrices require cautious interpretation even when factorization succeeds.'),
('component_interpretation','Component interpretation','Defines how factors modes singular vectors or components are connected to system meaning.','Prevents mathematical components from being mistaken for direct causal or institutional categories.','Components require domain review and sensitivity testing before substantive interpretation.'),
('responsible_use','Responsible use','Defines how factorization limits approximation loss diagnostics and assumptions are communicated.','Supports accountable systems analysis and reproducible scientific computing.','Decomposition results should be accompanied by method documentation and interpretation boundaries.');

CREATE TABLE decomposition_workflow_audit_cases (
    model_name TEXT NOT NULL,
    matrix_shape TEXT NOT NULL,
    matrix_class TEXT NOT NULL,
    recommended_workflow TEXT NOT NULL,
    condition_proxy REAL NOT NULL,
    estimated_rank INTEGER NOT NULL,
    singular_value_1 REAL NOT NULL,
    singular_value_2 REAL NOT NULL,
    singular_value_3 REAL NOT NULL,
    low_rank_reconstruction_error REAL NOT NULL,
    solve_residual_norm REAL NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO decomposition_workflow_audit_cases VALUES
('decomposition_workflow_audit','4x3','rectangular_overdetermined_dense_demo_matrix','QR_or_SVD_for_least_squares_and_rank_diagnostics',4.2,3,5.12,2.35,1.02,1.02,0.0,'Decomposition factors require rank conditioning reconstruction residual and interpretation review.');
