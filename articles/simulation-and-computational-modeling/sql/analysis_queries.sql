.headers on
.mode column

SELECT 'SIMULATION COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM simulation_component_type
ORDER BY component_type;

SELECT 'SIMULATION RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, computational_structure, review_question
FROM simulation_model_register
WHERE status IN ('review', 'revise');

SELECT 'SIMULATION SCENARIOS' AS section;
SELECT scenario, initial_stock, growth_rate, carrying_capacity, extraction, shock_probability, shock_fraction, steps, replications
FROM simulation_scenario
ORDER BY scenario;

SELECT 'SCENARIO STRESS CHECK' AS section;
SELECT
  scenario,
  ROUND(extraction / carrying_capacity, 3) AS extraction_to_capacity_ratio,
  ROUND(shock_probability * shock_fraction, 3) AS expected_shock_intensity,
  replications
FROM simulation_scenario
ORDER BY expected_shock_intensity DESC, extraction_to_capacity_ratio DESC;

SELECT 'SIMULATION COMPONENT GUIDE' AS section;
SELECT component_type, meaning, example, review_question
FROM simulation_component_guide
ORDER BY component_type;
