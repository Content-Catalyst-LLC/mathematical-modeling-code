.headers on
.mode column

SELECT 'CLIMATE FEEDBACK GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM climate_feedback_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM climate_feedback_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, model_type, interpretation, warning
FROM climate_feedback_scenario_records
ORDER BY scenario_name;
