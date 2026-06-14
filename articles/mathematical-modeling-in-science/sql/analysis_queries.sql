.headers on
.mode column

SELECT 'MODEL ROLE TYPES' AS section;
SELECT model_role, description, typical_failure
FROM model_role_type
ORDER BY model_role;

SELECT 'SCIENTIFIC MODEL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, scientific_domain, model_role, model_family, evidence_question
FROM scientific_model_register
WHERE status IN ('review', 'revise');

SELECT 'POPULATION SCENARIOS' AS section;
SELECT scenario_key, growth_rate, carrying_capacity, initial_population, years, observation_noise
FROM population_scenario
ORDER BY scenario_key;

SELECT 'DISCIPLINARY MODELING GUIDE' AS section;
SELECT scientific_field, modeling_use, typical_model_forms
FROM scientific_domain_guide
ORDER BY scientific_field;

SELECT 'HIGH-ATTENTION SCIENTIFIC REVIEW TARGETS' AS section;
SELECT record_key, scientific_domain, model_role, evidence_question
FROM scientific_model_register
WHERE model_role IN ('prediction', 'observation', 'model_comparison', 'uncertainty_quantification');
