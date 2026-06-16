.headers on
.mode column

SELECT 'ODE SOLVER ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM ode_solver_assumption_registry
ORDER BY assumption_key;

SELECT 'ODE SOLVER AUDIT CASES' AS section;
SELECT scenario, initial_value, decay_rate, step_size, stop_time, solver_method, absolute_tolerance, relative_tolerance, warning
FROM ode_solver_audit_cases
ORDER BY scenario;
