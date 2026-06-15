.headers on
.mode column

SELECT 'FIELD ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM field_assumption_registry
ORDER BY assumption_key;

SELECT 'FIELD AUDIT CASES' AS section;
SELECT scenario, grid_step, point_count, scalar_average, vector_magnitude_average, vector_magnitude_maximum, warning
FROM field_audit_cases
ORDER BY grid_step DESC;
