.headers on
.mode column

SELECT 'DOMAIN RULES' AS section;
SELECT * FROM domain_rule ORDER BY rule_key;

SELECT 'SCENARIO VALIDATION' AS section;
SELECT
    scenario_key,
    initial_state,
    growth_rate,
    capacity,
    time_horizon,
    CASE
        WHEN initial_state < 0 THEN 'review_initial_state'
        WHEN growth_rate < 0 THEN 'review_growth_rate'
        WHEN capacity <= 0 THEN 'review_capacity'
        WHEN time_horizon < 0 THEN 'review_time_horizon'
        WHEN initial_state > capacity THEN 'review_initial_exceeds_capacity'
        ELSE 'ok'
    END AS validation_status,
    interpretation
FROM model_scenario
ORDER BY scenario_key;
