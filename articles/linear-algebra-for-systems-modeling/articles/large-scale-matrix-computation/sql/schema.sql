DROP TABLE IF EXISTS matrix_computation_governance_registry;
DROP TABLE IF EXISTS large_scale_matrix_computation_audit_cases;

CREATE TABLE matrix_computation_governance_registry (
    assumption_key TEXT PRIMARY KEY,
    assumption_name TEXT NOT NULL,
    mathematical_role TEXT NOT NULL,
    systems_modeling_role TEXT NOT NULL,
    review_warning TEXT NOT NULL
);

INSERT INTO matrix_computation_governance_registry VALUES
('matrix_shape','Matrix shape','Defines row count column count and dimensional scale.','Determines memory runtime and algorithm feasibility.','Matrix dimensions should be reported before interpreting large-scale outputs.'),
('storage_format','Storage format','Defines dense sparse block distributed or matrix-free representation.','Controls what computations are efficient or possible.','Storage choices can affect runtime precision and reproducibility.'),
('sparsity_pattern','Sparsity pattern','Defines nonzero structure density locality and block relationships.','Reveals system connectivity and computational opportunity.','Sparse assumptions should reflect real structure rather than convenience alone.'),
('solver_choice','Solver choice','Defines direct iterative randomized or matrix-free computation.','Determines numerical behavior and scalability.','Solver choice should match matrix structure conditioning and required accuracy.'),
('convergence_diagnostics','Convergence diagnostics','Tracks residual norms tolerances iteration counts and stopping criteria.','Shows whether approximate results satisfy the intended system.','Stopping early or using weak tolerances can produce misleading outputs.'),
('conditioning_precision','Conditioning and precision','Defines sensitivity roundoff risk and numerical representation.','Determines whether computed results are stable under perturbation.','High condition numbers and low precision require special review.'),
('approximation_method','Approximation method','Defines low-rank randomized sketching sampling or matrix-free approximations.','Makes large problems tractable by preserving selected structure.','Approximation error should be measured and disclosed.'),
('responsible_use','Responsible use','Defines how scale approximation solver limits uncertainty and interpretation are communicated.','Prevents large computation from being mistaken for reliable evidence by size alone.','Large-scale output should be interpreted through model assumptions diagnostics and validation.');

CREATE TABLE large_scale_matrix_computation_audit_cases (
    model_name TEXT NOT NULL,
    matrix_dimension INTEGER NOT NULL,
    nonzero_entries INTEGER NOT NULL,
    density REAL NOT NULL,
    dense_storage_mb REAL NOT NULL,
    sparse_storage_mb_estimate REAL NOT NULL,
    storage_reduction_factor REAL NOT NULL,
    matrix_type TEXT NOT NULL,
    dominant_eigenvalue_estimate REAL NOT NULL,
    matrix_vector_product_norm REAL NOT NULL,
    iterative_residual_initial REAL NOT NULL,
    iterative_residual_final REAL NOT NULL,
    iterations INTEGER NOT NULL,
    warning TEXT NOT NULL
);

INSERT INTO large_scale_matrix_computation_audit_cases VALUES
('synthetic_large_scale_matrix_computation_audit',200,958,0.02395,0.32,0.015328,20.8768,'banded_sparse_like_symmetric_system',1.95,34.2,14.1,0.08,80,'Large-scale outputs are computational results under storage approximation precision solver and model assumptions.');
