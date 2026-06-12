.headers on
.mode column

SELECT 'SCENARIOS' AS section;
SELECT scenario, growth_rate, carrying_capacity, time_step, steps, description
FROM scenario_parameters
ORDER BY scenario;

SELECT 'ASSUMPTION REVIEW' AS section;
SELECT review_status, COUNT(*) AS assumption_count
FROM model_assumptions
GROUP BY review_status;

SELECT 'ASSUMPTIONS REQUIRING REVIEW' AS section;
SELECT assumption_key, risk_if_false, sensitivity_test
FROM model_assumptions
WHERE review_status IN ('review', 'revise');

SELECT 'DECISION RECORDS' AS section;
SELECT decision_title, modeling_choice, rationale, implications
FROM decision_records
ORDER BY record_id;
