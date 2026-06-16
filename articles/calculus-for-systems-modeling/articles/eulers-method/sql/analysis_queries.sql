.headers on
.mode column

SELECT 'EULER METHOD ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM euler_method_assumption_registry
ORDER BY assumption_key;

SELECT 'EULER METHOD AUDIT CASES' AS section;
SELECT scenario, initial_value, decay_rate, step_size, stop_time, stability_multiplier, stability_status, warning
FROM euler_method_audit_cases
ORDER BY scenario;
