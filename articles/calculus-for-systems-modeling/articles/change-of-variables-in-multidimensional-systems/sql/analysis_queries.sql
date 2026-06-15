.headers on
.mode column

SELECT 'CHANGE OF VARIABLES ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM change_of_variables_assumption_registry
ORDER BY assumption_key;

SELECT 'CHANGE OF VARIABLES CASES' AS section;
SELECT scenario, radius, radial_step, polar_total, cartesian_grid_total, relative_difference, jacobian_rule, warning
FROM change_of_variables_cases
ORDER BY radial_step DESC;
