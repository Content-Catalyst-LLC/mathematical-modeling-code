.headers on
.mode column

SELECT 'REPRODUCIBLE LINEAR ALGEBRA GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, workflow_role, documentation_role, review_warning
FROM reproducible_linear_algebra_governance_registry
ORDER BY assumption_key;

SELECT 'REPRODUCIBLE LINEAR ALGEBRA AUDIT CASES' AS section;
SELECT workflow_name, notebook_status, documentation_status, matrix_shape, matrix_meaning, data_provenance_status, environment_status, random_seed_status, validation_status, generated_outputs_status, residual_norm, relative_residual, reproducibility_score, warning
FROM reproducible_linear_algebra_audit_cases
ORDER BY workflow_name;
