.headers on
.mode column

SELECT 'RECURRENCE COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM recurrence_component_type
ORDER BY component_type;

SELECT 'RECURRENCE RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, expression, domain_or_step, review_question
FROM recurrence_model_register
WHERE status IN ('review', 'revise');

SELECT 'RECURRENCE SCENARIOS' AS section;
SELECT scenario, initial_storage, initial_demand, capacity, inflow, loss_rate, demand_response, periods, adaptive_demand
FROM recurrence_scenario
ORDER BY scenario;

SELECT 'ONE-STEP UPDATE CHECKS' AS section;
SELECT
  scenario,
  initial_storage,
  initial_storage + inflow - initial_demand - loss_rate * initial_storage AS raw_next_storage,
  CASE
    WHEN initial_storage + inflow - initial_demand - loss_rate * initial_storage < 0 THEN 0
    WHEN initial_storage + inflow - initial_demand - loss_rate * initial_storage > capacity THEN capacity
    ELSE initial_storage + inflow - initial_demand - loss_rate * initial_storage
  END AS bounded_next_storage
FROM recurrence_scenario
ORDER BY scenario;

SELECT 'RECURRENCE COMPONENT GUIDE' AS section;
SELECT component_type, meaning, example, review_question
FROM recurrence_component_guide
ORDER BY component_type;
