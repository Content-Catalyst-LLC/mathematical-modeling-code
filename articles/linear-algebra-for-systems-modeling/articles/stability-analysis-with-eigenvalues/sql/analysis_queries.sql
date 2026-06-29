.headers on
.mode column

SELECT 'STABILITY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM stability_assumption_registry
ORDER BY assumption_key;

SELECT 'STABILITY ANALYSIS AUDIT CASES' AS section;
SELECT system_name, spectral_radius, largest_real_part, discrete_time_classification, continuous_time_classification, warning
FROM stability_analysis_audit_cases
ORDER BY system_name;
