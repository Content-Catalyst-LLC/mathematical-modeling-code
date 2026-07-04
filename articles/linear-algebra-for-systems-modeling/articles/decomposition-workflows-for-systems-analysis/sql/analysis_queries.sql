.headers on
.mode column

SELECT 'DECOMPOSITION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, workflow_role, review_warning
FROM decomposition_governance_registry
ORDER BY assumption_key;

SELECT 'DECOMPOSITION WORKFLOW AUDIT CASES' AS section;
SELECT model_name, matrix_shape, matrix_class, recommended_workflow, condition_proxy, estimated_rank, singular_value_1, singular_value_2, singular_value_3, low_rank_reconstruction_error, solve_residual_norm, warning
FROM decomposition_workflow_audit_cases
ORDER BY model_name;
