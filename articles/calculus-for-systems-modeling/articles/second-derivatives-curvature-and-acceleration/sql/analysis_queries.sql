.headers on
.mode column

SELECT 'SECOND DERIVATIVE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM second_derivative_assumption_registry
ORDER BY assumption_key;
