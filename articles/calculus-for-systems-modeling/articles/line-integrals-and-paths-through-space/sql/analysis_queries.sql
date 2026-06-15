.headers on
.mode column

SELECT 'LINE INTEGRAL ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM line_integral_assumption_registry
ORDER BY assumption_key;

SELECT 'LINE INTEGRAL AUDIT CASES' AS section;
SELECT scenario, time_step, point_count, path_length, scalar_line_integral, vector_line_integral, average_alignment, warning
FROM line_integral_audit_cases
ORDER BY time_step DESC;
