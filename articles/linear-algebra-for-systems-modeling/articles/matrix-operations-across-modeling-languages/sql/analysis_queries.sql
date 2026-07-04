.headers on
.mode column

SELECT 'MATRIX OPERATION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, implementation_role, review_warning
FROM matrix_operation_governance_registry
ORDER BY assumption_key;

SELECT 'CROSS LANGUAGE MATRIX AUDIT CASES' AS section;
SELECT model_name, language, matrix_shape, vector_shape, indexing_convention, matrix_multiplication_operator, elementwise_operator, solve_method, condition_number, matrix_vector_product_norm, matrix_matrix_product_trace, solve_residual_norm, determinant, validation_status, warning
FROM cross_language_matrix_audit_cases
ORDER BY language;
