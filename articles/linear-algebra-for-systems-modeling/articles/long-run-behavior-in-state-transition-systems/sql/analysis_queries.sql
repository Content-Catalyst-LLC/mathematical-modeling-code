.headers on
.mode column

SELECT 'LONG-RUN TRANSITION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM long_run_transition_assumption_registry
ORDER BY assumption_key;

SELECT 'LONG-RUN TRANSITION AUDIT CASES' AS section;
SELECT system_name, states, stationary_estimate, convergence_distance_a, convergence_distance_b, initial_condition_gap_after_25_steps, warning
FROM long_run_transition_audit_cases
ORDER BY system_name;
