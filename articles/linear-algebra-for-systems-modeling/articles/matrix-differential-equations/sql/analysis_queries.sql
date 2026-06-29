.headers on
.mode column

SELECT 'MATRIX DIFFERENTIAL ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM matrix_differential_assumption_registry
ORDER BY assumption_key;

SELECT 'MATRIX DIFFERENTIAL AUDIT CASES' AS section;
SELECT system_name, time_horizon, final_state_estimate, max_real_part, stability_classification, warning
FROM matrix_differential_audit_cases
ORDER BY system_name;
