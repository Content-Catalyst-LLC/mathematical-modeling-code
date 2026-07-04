DROP TABLE IF EXISTS sparse_matrix_governance_registry;
DROP TABLE IF EXISTS sparse_matrix_efficiency_audit_cases;

CREATE TABLE sparse_matrix_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO sparse_matrix_governance_registry VALUES
('matrix_shape','Matrix shape','Defines row count column count and dimensional scale.','Determines memory runtime and algorithm feasibility.','Shape should be reported before making efficiency or interpretation claims.'),
('nonzero_structure','Nonzero structure','Defines locations and values of stored relationships.','Represents modeled connectivity dependence constraints or feature presence.','The sparsity pattern should be reviewed as system structure not only storage detail.'),
('zero_interpretation','Zero interpretation','Defines what missing entries mean mathematically.','Distinguishes absent unknown ignored thresholded or impossible relationships.','Zeros can encode assumptions that affect evidence and decisions.'),
('storage_format','Storage format','Defines COO CSR CSC DIA BSR graph or matrix-free representation.','Controls construction multiplication factorization and solver efficiency.','Storage format should match the workflow not only the dataset.'),
('solver_choice','Solver choice','Defines direct sparse factorization iterative method or preconditioned solver.','Determines scalability convergence memory use and numerical behavior.','Solver choice should match matrix symmetry conditioning sparsity and accuracy needs.'),
('fill_in_risk','Fill-in risk','Tracks whether sparse factorization creates many additional nonzero entries.','Determines whether direct solving remains efficient.','Ordering and symbolic analysis should be documented for large sparse factorizations.'),
('thresholding_rule','Thresholding rule','Defines when small values are converted to zeros.','Controls model simplification and computational efficiency.','Thresholds may remove weak but important relationships or rare signals.'),
('responsible_use','Responsible use','Defines how sparsity omitted relationships efficiency stability and validation are communicated.','Prevents sparse computation from being mistaken for complete system representation.','Sparse outputs should be interpreted through structure omissions diagnostics and validation.');

CREATE TABLE sparse_matrix_efficiency_audit_cases (
    model_name TEXT NOT NULL,
    matrix_dimension INTEGER NOT NULL,
    nonzero_entries INTEGER NOT NULL,
    density REAL NOT NULL,
    dense_storage_mb REAL NOT NULL,
    coordinate_storage_mb_estimate REAL NOT NULL,
    storage_reduction_factor REAL NOT NULL,
    average_row_degree REAL NOT NULL,
    max_row_degree INTEGER NOT NULL,
    isolated_rows INTEGER NOT NULL,
    matrix_vector_product_norm REAL NOT NULL,
    iterative_residual_initial REAL NOT NULL,
    iterative_residual_final REAL NOT NULL,
    iterations INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO sparse_matrix_efficiency_audit_cases VALUES
('synthetic_sparse_matrix_efficiency_audit',250,1244,0.019904,0.5,0.019904,25.12,3.98,6,0,31.6,15.8,0.06,60,'Sparse outputs should be interpreted through structure omissions diagnostics and validation.');
