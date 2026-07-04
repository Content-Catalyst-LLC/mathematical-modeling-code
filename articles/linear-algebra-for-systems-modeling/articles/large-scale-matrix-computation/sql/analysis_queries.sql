.headers on
.mode column

SELECT 'MATRIX COMPUTATION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM matrix_computation_governance_registry
ORDER BY assumption_key;

SELECT 'LARGE SCALE MATRIX COMPUTATION AUDIT CASES' AS section;
SELECT model_name, matrix_dimension, nonzero_entries, density, dense_storage_mb, sparse_storage_mb_estimate, storage_reduction_factor, matrix_type, dominant_eigenvalue_estimate, matrix_vector_product_norm, iterative_residual_initial, iterative_residual_final, iterations, warning
FROM large_scale_matrix_computation_audit_cases;
