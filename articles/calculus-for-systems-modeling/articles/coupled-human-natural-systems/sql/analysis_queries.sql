.headers on
.mode column

SELECT 'COUPLED SYSTEMS GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM coupled_systems_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM coupled_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, model_type, final_human_pressure, final_natural_stock, cumulative_extraction, cumulative_burden, interpretation, warning
FROM coupled_scenario_records
ORDER BY scenario_name;

SELECT 'DIAGNOSTIC RECORDS' AS section;
SELECT diagnostic_name, value, unit, interpretation, warning
FROM coupled_diagnostic_records
ORDER BY diagnostic_name;
