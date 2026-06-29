.headers on
.mode column

SELECT 'MARKOV ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM markov_assumption_registry
ORDER BY assumption_key;

SELECT 'MARKOV TRANSITION AUDIT CASES' AS section;
SELECT system_name, states, orientation, row_sum_error, nonnegative, one_step_distribution, steady_state_estimate, warning
FROM markov_transition_audit_cases
ORDER BY system_name;
