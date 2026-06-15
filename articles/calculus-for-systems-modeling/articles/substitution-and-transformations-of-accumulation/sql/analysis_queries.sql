.headers on
.mode column

SELECT 'SUBSTITUTION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM substitution_assumption_registry
ORDER BY assumption_key;
