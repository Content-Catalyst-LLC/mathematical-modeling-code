.headers on
.mode column

SELECT 'LINEAR DYNAMICS ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM linear_dynamics_assumption_registry
ORDER BY assumption_key;

SELECT 'LINEAR DYNAMICS AUDIT CASES' AS section;
SELECT system_name, horizon, final_state, spectral_radius, stability_classification, warning
FROM linear_dynamics_audit_cases
ORDER BY system_name;
