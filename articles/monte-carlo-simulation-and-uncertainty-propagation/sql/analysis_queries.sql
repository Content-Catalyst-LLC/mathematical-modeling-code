.headers on
.mode column

SELECT 'MONTE CARLO COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM monte_carlo_component_type
ORDER BY component_type;

SELECT 'MONTE CARLO RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, uncertainty_structure, review_question
FROM monte_carlo_model_register
WHERE status IN ('review', 'revise');

SELECT 'MONTE CARLO SCENARIOS' AS section;
SELECT scenario, initial_stock_min, initial_stock_max, growth_rate_min, growth_rate_max, extraction_min, extraction_max, shock_probability_min, shock_probability_max, replications, seed
FROM monte_carlo_scenario
ORDER BY scenario;

SELECT 'UNCERTAINTY RANGE CHECK' AS section;
SELECT
  scenario,
  ROUND(initial_stock_max - initial_stock_min, 4) AS initial_stock_range,
  ROUND(growth_rate_max - growth_rate_min, 4) AS growth_rate_range,
  ROUND(extraction_max - extraction_min, 4) AS extraction_range,
  ROUND(shock_probability_max - shock_probability_min, 4) AS shock_probability_range,
  replications
FROM monte_carlo_scenario
ORDER BY scenario;

SELECT 'MONTE CARLO COMPONENT GUIDE' AS section;
SELECT component_type, meaning, example, review_question
FROM monte_carlo_component_guide
ORDER BY component_type;
