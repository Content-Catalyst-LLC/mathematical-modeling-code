.headers on
.mode column
SELECT 'POPULATION MODEL GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning FROM population_model_governance_registry ORDER BY registry_key;
SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, source_status, interpretation, warning FROM population_parameter_records ORDER BY parameter_name;
SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, model_type, interpretation, warning FROM population_scenario_records ORDER BY scenario_name;
SELECT 'IDENTIFIABILITY RECORDS' AS section;
SELECT diagnostic_name, issue, warning, governance_response FROM population_identifiability_records ORDER BY diagnostic_name;
