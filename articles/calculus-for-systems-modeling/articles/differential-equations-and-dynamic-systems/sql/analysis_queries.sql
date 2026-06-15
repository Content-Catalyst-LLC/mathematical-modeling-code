.headers on
.mode column

SELECT 'DIFFERENTIAL EQUATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM differential_equation_assumption_registry
ORDER BY assumption_key;

SELECT 'DYNAMIC SYSTEM AUDIT CASES' AS section;
SELECT scenario, model_type, initial_state, growth_rate, carrying_capacity, time_step, steps, method, warning
FROM dynamic_system_audit_cases
ORDER BY scenario;
