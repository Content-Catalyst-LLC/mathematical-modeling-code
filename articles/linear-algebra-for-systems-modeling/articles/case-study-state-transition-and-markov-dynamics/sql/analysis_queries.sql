.headers on
.mode column

SELECT 'MARKOV GOVERNANCE REGISTRY' AS section;
SELECT governance_name, modeling_role, review_requirement, responsible_use_warning
FROM state_transition_markov_governance_registry
ORDER BY governance_key;

SELECT 'TRANSITION MATRIX ROW SUMS' AS section;
SELECT current_state, scenario_name, ROUND(SUM(transition_probability), 6) AS row_sum
FROM transition_matrix
GROUP BY current_state, scenario_name
ORDER BY current_state;

SELECT 'STATE TRANSITION MARKOV AUDIT CASES' AS section;
SELECT workflow_name, scenario_name, state_count, time_steps, stochastic_check_passed, initial_primary_state, highest_probability_state_after_horizon, highest_probability_after_horizon, stationary_highest_probability_state, stationary_highest_probability, baseline_disrupted_probability_after_horizon, stress_disrupted_probability_after_horizon, memoryless_warning, interpretation_warning
FROM state_transition_markov_audit_cases
ORDER BY workflow_name;
