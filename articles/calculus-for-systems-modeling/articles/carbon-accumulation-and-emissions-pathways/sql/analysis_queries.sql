.headers on
.mode column

SELECT 'CARBON PATHWAY GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM carbon_pathway_governance_registry
ORDER BY registry_key;

SELECT 'PARAMETER RECORDS' AS section;
SELECT parameter_name, value, unit, interpretation, warning
FROM carbon_pathway_parameter_records
ORDER BY parameter_name;

SELECT 'SCENARIO RECORDS' AS section;
SELECT scenario_name, pathway_type, cumulative_emissions, atmospheric_burden, interpretation, warning
FROM carbon_pathway_scenario_records
ORDER BY scenario_name;

SELECT 'BUDGET RECORDS' AS section;
SELECT scenario_name, cumulative_emissions, budget, exceeds_budget, warning
FROM carbon_budget_records
ORDER BY scenario_name;
