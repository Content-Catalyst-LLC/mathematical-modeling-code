.headers on
.mode column

SELECT 'ECOLOGY MODEL ROLE TYPES' AS section;
SELECT model_role, description, typical_failure
FROM ecology_model_role_type
ORDER BY model_role;

SELECT 'ECOLOGY MODEL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, domain, model_role, model_family, sustainability_question
FROM ecology_model_register
WHERE status IN ('review', 'revise');

SELECT 'RESOURCE SCENARIOS' AS section;
SELECT
  scenario_key,
  scenario_name,
  initial_stock,
  growth_rate,
  carrying_capacity,
  extraction,
  climate_stress,
  minimum_stock,
  ROUND(growth_rate * (1.0 - climate_stress), 4) AS effective_growth_rate
FROM resource_scenario
ORDER BY scenario_key;

SELECT 'ECOLOGY DOMAIN GUIDE' AS section;
SELECT area, modeling_use, typical_model_forms
FROM ecology_domain_guide
ORDER BY area;

SELECT 'HIGH-ATTENTION SUSTAINABILITY REVIEW TARGETS' AS section;
SELECT record_key, domain, model_role, sustainability_question
FROM ecology_model_register
WHERE model_role IN ('threshold_review', 'scenario_analysis', 'network_review', 'adaptive_management');
