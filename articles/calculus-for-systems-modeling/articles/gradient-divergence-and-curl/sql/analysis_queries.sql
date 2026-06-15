.headers on
.mode column

SELECT 'FIELD OPERATOR ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM field_operator_assumption_registry
ORDER BY assumption_key;

SELECT 'FIELD OPERATOR AUDIT CASES' AS section;
SELECT scenario, grid_step, point_count, mean_gradient_magnitude, maximum_gradient_magnitude, mean_divergence, mean_curl, warning
FROM field_operator_audit_cases
ORDER BY grid_step DESC;
