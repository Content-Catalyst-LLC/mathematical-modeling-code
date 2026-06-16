.headers on
.mode column

SELECT 'PREDATOR-PREY GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM predator_prey_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM predator_prey_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, model_type, interpretation, warning
FROM predator_prey_scenario_records
ORDER BY scenario_name;

SELECT 'NULLCLINE RECORDS' AS section;
SELECT nullcline_name, equation, interpretation, warning
FROM predator_prey_nullcline_records
ORDER BY nullcline_name;
