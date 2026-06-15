.headers on
.mode column

SELECT 'CHAIN RULE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM chain_rule_assumption_registry
ORDER BY assumption_key;
