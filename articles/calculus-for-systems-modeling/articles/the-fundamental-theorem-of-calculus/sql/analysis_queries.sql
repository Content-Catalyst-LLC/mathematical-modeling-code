.headers on
.mode column

SELECT 'FUNDAMENTAL THEOREM ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM fundamental_theorem_assumption_registry
ORDER BY assumption_key;
