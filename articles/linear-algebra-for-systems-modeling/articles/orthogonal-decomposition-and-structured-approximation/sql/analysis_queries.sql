.headers on
.mode column

SELECT 'DECOMPOSITION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM decomposition_governance_registry
ORDER BY assumption_key;

SELECT 'ORTHOGONAL APPROXIMATION AUDIT CASES' AS section;
SELECT model_name, rows, columns, numerical_rank, condition_number, residual_norm, relative_residual_norm, orthogonality_error, coefficient_norm, method, warning
FROM orthogonal_approximation_audit_cases
ORDER BY model_name;
