.headers on
.mode column

SELECT 'INFRASTRUCTURE GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM infrastructure_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM infrastructure_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, system_type, final_queue, average_utilization, maximum_delay, interpretation, warning
FROM infrastructure_scenario_records
ORDER BY scenario_name;

SELECT 'BOTTLENECK RECORDS' AS section;
SELECT record_name, stage_capacities, effective_capacity, bottleneck_stage, warning
FROM infrastructure_bottleneck_records
ORDER BY record_name;
