.headers on
.mode column

SELECT 'ASSUMPTION TYPES' AS section;
SELECT assumption_type, description, typical_test
FROM assumption_type
ORDER BY assumption_type;

SELECT 'ASSUMPTIONS REQUIRING REVIEW' AS section;
SELECT assumption_key, assumption_type, risk_if_false, sensitivity_test
FROM assumption_register
WHERE review_status IN ('review', 'revise');

SELECT 'HIGH PRIORITY SENSITIVITY TESTS' AS section;
SELECT assumption_key, test_name, low_case, high_case
FROM sensitivity_plan
WHERE review_priority = 'high';

SELECT 'SCENARIOS' AS section;
SELECT scenario, initial_stock, capacity, inflow, demand, loss_rate, periods
FROM scenario_parameter
ORDER BY scenario;

SELECT 'DESIGN RECORDS' AS section;
SELECT design_choice, rationale, limitation, revision_trigger
FROM model_design_record;
