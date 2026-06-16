.headers on
.mode column

SELECT 'ECONOMIC GROWTH GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM economic_growth_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM economic_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, model_type, final_output, final_capital, interpretation, warning
FROM economic_scenario_records
ORDER BY scenario_name;

SELECT 'GROWTH RECORDS' AS section;
SELECT record_name, growth_rate, horizon, final_output, doubling_time, warning
FROM economic_growth_records
ORDER BY growth_rate;
