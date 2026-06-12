.headers on
.mode column

SELECT 'STATE TYPES' AS section;
SELECT state_type, description, typical_failure
FROM state_type
ORDER BY state_type;

SELECT 'STATE RECORDS REQUIRING REVIEW' AS section;
SELECT state_key, state_type, unit, observability, review_question
FROM state_variable_register
WHERE status IN ('review', 'revise');

SELECT 'REPRESENTATION SCENARIOS' AS section;
SELECT scenario, representation, initial_storage, initial_demand, initial_condition, capacity, inflow, loss_rate, periods
FROM representation_scenario
ORDER BY scenario;

SELECT 'VARIABLE ROLE GUIDE' AS section;
SELECT role, meaning, example, review_question
FROM variable_role_guide
ORDER BY role;
