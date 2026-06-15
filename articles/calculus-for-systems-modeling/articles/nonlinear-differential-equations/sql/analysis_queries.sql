.headers on
.mode column

SELECT 'NONLINEAR ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM nonlinear_assumption_registry
ORDER BY assumption_key;

SELECT 'NONLINEAR AUDIT CASES' AS section;
SELECT scenario, initial_state, parameter_a, parameter_b, parameter_c, time_step, steps, method, warning
FROM nonlinear_audit_cases
ORDER BY scenario;
