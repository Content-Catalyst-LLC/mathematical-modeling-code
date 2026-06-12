.headers on
.mode column

SELECT 'MODELING STAGES' AS section;
SELECT stage_order, stage_name, guiding_question, expected_artifact
FROM modeling_stage
ORDER BY stage_order;

SELECT 'SCENARIOS' AS section;
SELECT scenario, base_inflow, base_demand, demand_growth, loss_rate, description
FROM scenario_parameter
ORDER BY scenario;

SELECT 'ASSUMPTION REVIEW' AS section;
SELECT review_status, COUNT(*) AS assumption_count
FROM assumption_register
GROUP BY review_status;

SELECT 'ASSUMPTIONS REQUIRING REVIEW' AS section;
SELECT assumption_key, risk_if_false, sensitivity_test
FROM assumption_register
WHERE review_status IN ('review', 'revise');
