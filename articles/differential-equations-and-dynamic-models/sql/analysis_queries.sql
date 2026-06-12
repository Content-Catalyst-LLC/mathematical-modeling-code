.headers on
.mode column

SELECT 'DYNAMIC COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM dynamic_component_type
ORDER BY component_type;

SELECT 'DYNAMIC RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, expression, units_or_domain, review_question
FROM dynamic_model_register
WHERE status IN ('review', 'revise');

SELECT 'DYNAMIC SCENARIOS' AS section;
SELECT scenario, initial_storage, capacity, inflow_rate, demand_rate, loss_rate, dt, horizon
FROM dynamic_scenario
ORDER BY scenario;

SELECT 'ONE-STEP RATE CHECKS' AS section;
SELECT
  scenario,
  initial_storage,
  inflow_rate - demand_rate - loss_rate * initial_storage AS initial_rate,
  initial_storage + dt * (inflow_rate - demand_rate - loss_rate * initial_storage) AS euler_one_step_storage
FROM dynamic_scenario
ORDER BY scenario;

SELECT 'DYNAMIC COMPONENT GUIDE' AS section;
SELECT component_type, meaning, example, review_question
FROM dynamic_component_guide
ORDER BY component_type;
