.headers on
.mode column

SELECT 'TOTAL DIFFERENTIAL ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM total_differential_assumption_registry
ORDER BY assumption_key;

SELECT 'TOTAL DIFFERENTIAL CASES' AS section;
SELECT x, y, dx, dy, actual_change, differential_estimate, absolute_error, feasible_displacement, warning
FROM total_differential_cases
ORDER BY x, y, dx, dy;
