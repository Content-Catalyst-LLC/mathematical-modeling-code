.headers on
.mode column

SELECT 'DELAY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM delay_assumption_registry
ORDER BY assumption_key;

SELECT 'DELAY AUDIT CASES' AS section;
SELECT scenario, initial_state, target, adjustment_rate, delay, dt, steps, warning
FROM delay_audit_cases
ORDER BY scenario;
