.headers on
.mode column

SELECT 'RUNGE-KUTTA ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM runge_kutta_assumption_registry
ORDER BY assumption_key;

SELECT 'RUNGE-KUTTA AUDIT CASES' AS section;
SELECT scenario, initial_value, decay_rate, step_size, stop_time, method_family, warning
FROM runge_kutta_audit_cases
ORDER BY scenario;
