.headers on
.mode column

SELECT 'SCIENTIFIC COMPUTING GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, computational_role, workflow_role, review_warning
FROM scientific_computing_governance_registry
ORDER BY assumption_key;

SELECT 'SCIENTIFIC COMPUTING LINEAR ALGEBRA AUDIT CASES' AS section;
SELECT model_name, workflow_stage, matrix_shape, representation, precision, solver_choice, tolerance, determinant, condition_number_proxy, matrix_vector_norm, solution_norm, residual_norm, relative_residual, reproducibility_status, warning
FROM scientific_computing_linear_algebra_audit_cases
ORDER BY model_name;
