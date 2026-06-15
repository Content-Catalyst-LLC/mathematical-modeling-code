.headers on
.mode column

SELECT 'IMPROPER INTEGRAL ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM improper_integral_assumption_registry
ORDER BY assumption_key;
