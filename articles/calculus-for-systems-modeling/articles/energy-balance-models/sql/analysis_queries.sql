.headers on
.mode column

SELECT 'ENERGY BALANCE GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM energy_balance_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM energy_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, model_type, final_temperature, equilibrium_temperature, adjustment_time, interpretation, warning
FROM energy_scenario_records
ORDER BY scenario_name;

SELECT 'DIAGNOSTIC RECORDS' AS section;
SELECT diagnostic_name, value, unit, interpretation, warning
FROM energy_diagnostic_records
ORDER BY diagnostic_name;
