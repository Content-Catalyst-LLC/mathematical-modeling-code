.headers on
.mode column

SELECT 'EPIDEMIOLOGICAL GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM epidemiological_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM epidemiological_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, model_type, peak_infectious, final_recovered, reproduction_number, interpretation, warning
FROM epidemiological_scenario_records
ORDER BY scenario_name;

SELECT 'THRESHOLD RECORDS' AS section;
SELECT record_name, r0, susceptible_threshold, herd_immunity_threshold, doubling_time, warning
FROM epidemiological_threshold_records
ORDER BY record_name;
