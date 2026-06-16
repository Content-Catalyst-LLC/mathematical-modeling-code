.headers on
.mode column

SELECT 'FINANCIAL GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM financial_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM financial_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, model_type, final_value, present_value, interpretation, warning
FROM financial_scenario_records
ORDER BY scenario_name;

SELECT 'RATE RECORDS' AS section;
SELECT record_name, nominal_rate, inflation_rate, real_rate, continuous_equivalent, warning
FROM financial_rate_records
ORDER BY record_name;
