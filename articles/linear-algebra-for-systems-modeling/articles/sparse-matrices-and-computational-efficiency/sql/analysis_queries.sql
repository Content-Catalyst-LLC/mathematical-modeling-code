.headers on
.mode column

SELECT 'SPARSE MATRIX GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM sparse_matrix_governance_registry
ORDER BY assumption_key;

SELECT 'SPARSE MATRIX EFFICIENCY AUDIT CASES' AS section;
SELECT model_name, matrix_dimension, nonzero_entries, density, dense_storage_mb, coordinate_storage_mb_estimate, storage_reduction_factor, average_row_degree, max_row_degree, isolated_rows, matrix_vector_product_norm, iterative_residual_initial, iterative_residual_final, iterations, warning
FROM sparse_matrix_efficiency_audit_cases
ORDER BY model_name;
