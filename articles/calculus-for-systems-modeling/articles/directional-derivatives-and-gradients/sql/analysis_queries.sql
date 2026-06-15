.headers on
.mode column

SELECT 'DIRECTIONAL DERIVATIVE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM directional_derivative_assumption_registry
ORDER BY assumption_key;

SELECT 'DIRECTIONAL DERIVATIVE CASES' AS section;
SELECT x, y, direction_x, direction_y, gradient_x, gradient_y, directional_derivative, step_size, absolute_error, feasible_direction, warning
FROM directional_derivative_cases
ORDER BY x, y, direction_x, direction_y;
