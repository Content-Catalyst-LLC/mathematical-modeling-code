.headers on
.mode column

SELECT 'SHOCK ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM shock_assumption_registry
ORDER BY assumption_key;

SELECT 'FORCED SYSTEM AUDIT CASES' AS section;
SELECT scenario, initial_state, equilibrium, recovery_rate, shock_time, shock_magnitude, dt, steps, warning
FROM forced_system_audit_cases
ORDER BY scenario;
