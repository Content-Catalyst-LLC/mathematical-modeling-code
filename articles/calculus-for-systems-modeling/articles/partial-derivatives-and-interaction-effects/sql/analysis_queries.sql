.headers on
.mode column

SELECT 'PARTIAL DERIVATIVE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM partial_derivative_assumption_registry
ORDER BY assumption_key;

SELECT 'PARTIAL DERIVATIVE CASES' AS section;
SELECT x, y, output, partial_x, partial_y, cross_partial_xy, feasible, warning
FROM partial_derivative_cases
ORDER BY x, y;
