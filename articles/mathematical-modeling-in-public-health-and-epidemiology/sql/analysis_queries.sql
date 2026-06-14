.headers on
.mode column

SELECT 'PUBLIC HEALTH MODEL ROLE TYPES' AS section;
SELECT model_role, description, typical_failure
FROM public_health_model_role_type
ORDER BY model_role;

SELECT 'PUBLIC HEALTH MODEL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, domain, model_role, model_family, public_health_question
FROM public_health_model_register
WHERE status IN ('review', 'revise');

SELECT 'EPIDEMIC SCENARIOS' AS section;
SELECT
  scenario_key,
  scenario_name,
  population,
  beta,
  gamma,
  ROUND(beta / gamma, 3) AS r0_simple,
  hospital_capacity,
  hospitalization_rate
FROM epidemic_scenario
ORDER BY r0_simple DESC;

SELECT 'PUBLIC HEALTH DOMAIN GUIDE' AS section;
SELECT area, modeling_use, typical_model_forms
FROM public_health_domain_guide
ORDER BY area;

SELECT 'HIGH-ATTENTION PUBLIC HEALTH REVIEW TARGETS' AS section;
SELECT record_key, domain, model_role, public_health_question
FROM public_health_model_register
WHERE model_role IN ('data_interpretation', 'capacity_review', 'distributional_review', 'uncertainty_communication');
