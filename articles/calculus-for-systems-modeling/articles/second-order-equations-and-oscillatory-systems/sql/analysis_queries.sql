.headers on
.mode column

SELECT 'SECOND-ORDER ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM second_order_assumption_registry
ORDER BY assumption_key;

SELECT 'SECOND-ORDER AUDIT CASES' AS section;
SELECT scenario, initial_position, initial_velocity, damping_ratio, natural_frequency, forcing_amplitude, forcing_frequency, time_step, steps, method, warning
FROM second_order_audit_cases
ORDER BY scenario;
