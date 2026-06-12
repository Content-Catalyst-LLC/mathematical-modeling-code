-- Diagnostic queries for modeling metadata.

SELECT
    scenario,
    growth_rate,
    carrying_capacity,
    time_step,
    steps,
    description
FROM scenario_parameters
ORDER BY scenario;

SELECT
    review_status,
    COUNT(*) AS assumption_count
FROM model_assumptions
GROUP BY review_status;

SELECT
    decision_title,
    modeling_choice,
    rationale,
    implications
FROM decision_records
ORDER BY record_id;
