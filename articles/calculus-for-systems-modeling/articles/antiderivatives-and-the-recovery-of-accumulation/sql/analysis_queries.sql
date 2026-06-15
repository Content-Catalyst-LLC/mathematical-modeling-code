.headers on
.mode column

SELECT 'ANTIDERIVATIVE RECOVERY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM antiderivative_recovery_assumption_registry
ORDER BY assumption_key;
