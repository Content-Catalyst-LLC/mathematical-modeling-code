.headers on
.mode column

SELECT 'INTEGRATION BY PARTS ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM integration_by_parts_assumption_registry
ORDER BY assumption_key;
