.headers on
.mode column

SELECT 'SENSITIVITY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM sensitivity_assumption_registry
ORDER BY assumption_key;
