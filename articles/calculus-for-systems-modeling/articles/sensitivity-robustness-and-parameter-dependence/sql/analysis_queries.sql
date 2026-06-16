.headers on
.mode column

SELECT 'SENSITIVITY GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM sensitivity_governance_registry
ORDER BY registry_key;

SELECT 'SENSITIVITY RECORDS' AS section;
SELECT parameter_name, baseline_value, lower_bound, upper_bound, sensitivity_status, warning
FROM sensitivity_records
ORDER BY parameter_name;
