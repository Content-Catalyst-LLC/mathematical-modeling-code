.headers on
.mode column

SELECT 'COUPLED SYSTEM ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM coupled_system_assumption_registry
ORDER BY assumption_key;

SELECT 'COUPLED SYSTEM AUDIT CASES' AS section;
SELECT scenario, prey0, predator0, alpha, beta, delta, gamma, time_step, steps, method, warning
FROM coupled_system_audit_cases
ORDER BY scenario;
