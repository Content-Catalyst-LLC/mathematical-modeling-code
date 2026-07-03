.headers on
.mode column

SELECT 'SIMULATION GOVERNANCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM simulation_governance_registry
ORDER BY assumption_key;

SELECT 'HIGH DIMENSIONAL SIMULATION AUDIT CASES' AS section;
SELECT model_name, state_dimension, time_steps, ensemble_runs, method, random_seed, transition_spectral_radius, transition_density, final_state_mean_norm, final_state_mean_total, final_state_95th_percentile_total, threshold_exceedance_probability, first_three_component_energy, warning
FROM high_dimensional_simulation_audit_cases
ORDER BY model_name;
