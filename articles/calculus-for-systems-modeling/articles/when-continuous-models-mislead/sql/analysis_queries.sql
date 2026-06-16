.headers on
.mode column

SELECT 'CONTINUOUS MODEL GOVERNANCE REGISTRY' AS section;
SELECT registry_name, analytical_role, systems_modeling_role, review_warning
FROM continuous_model_governance_registry
ORDER BY registry_key;

SELECT 'CONTINUOUS MODEL RISKS' AS section;
SELECT risk_name, risk_pattern, possible_consequence, governance_response, review_status
FROM continuous_model_risks
ORDER BY risk_name;
