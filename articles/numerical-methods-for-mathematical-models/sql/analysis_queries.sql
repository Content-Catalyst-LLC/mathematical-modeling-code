.headers on
.mode column

SELECT 'NUMERICAL COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM numerical_component_type
ORDER BY component_type;

SELECT 'NUMERICAL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, numerical_structure, review_question
FROM numerical_method_register
WHERE status IN ('review', 'revise');

SELECT 'SOLVER SCENARIOS' AS section;
SELECT scenario, initial_stock, growth_rate, carrying_capacity, extraction, horizon, step_size
FROM solver_scenario
ORDER BY step_size DESC;

SELECT 'DISCRETIZATION CHECK' AS section;
SELECT
  scenario,
  step_size,
  ROUND(horizon / step_size, 0) AS implied_steps,
  ROUND(extraction / carrying_capacity, 4) AS extraction_to_capacity_ratio
FROM solver_scenario
ORDER BY step_size DESC;

SELECT 'NUMERICAL COMPONENT GUIDE' AS section;
SELECT component_type, meaning, example, review_question
FROM numerical_component_guide
ORDER BY component_type;
