.headers on
.mode column

SELECT 'RESOURCE GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM resource_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM resource_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, resource_type, final_stock, cumulative_extraction, interpretation, warning
FROM resource_scenario_records
ORDER BY scenario_name;

SELECT 'YIELD RECORDS' AS section;
SELECT record_name, maximum_sustainable_yield, precautionary_yield, warning
FROM resource_yield_records
ORDER BY record_name;
