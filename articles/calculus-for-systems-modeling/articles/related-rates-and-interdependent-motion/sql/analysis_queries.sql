.headers on
.mode column

SELECT 'RELATED RATES ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM related_rates_assumption_registry
ORDER BY assumption_key;
