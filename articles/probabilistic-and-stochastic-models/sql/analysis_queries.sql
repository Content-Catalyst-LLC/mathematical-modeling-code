.headers on
.mode column

SELECT 'PROBABILITY COMPONENT TYPES' AS section;
SELECT model_component, description, typical_failure
FROM probability_component_type
ORDER BY model_component;

SELECT 'PROBABILITY RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, model_component, distribution_or_rule, review_question
FROM probability_model_register
WHERE status IN ('review', 'revise');

SELECT 'RISK SCENARIOS' AS section;
SELECT scenario, demand_mu, demand_sigma, supply_mean, supply_sd, reserve, simulations, seed
FROM risk_scenario
ORDER BY scenario;

SELECT 'APPROXIMATE DETERMINISTIC CHECKS' AS section;
SELECT
  scenario,
  exp(demand_mu + 0.5 * demand_sigma * demand_sigma) AS expected_lognormal_demand,
  supply_mean + reserve AS expected_available_supply,
  CASE
    WHEN exp(demand_mu + 0.5 * demand_sigma * demand_sigma) > supply_mean + reserve
    THEN 'mean demand exceeds expected available supply'
    ELSE 'mean demand below expected available supply'
  END AS mean_risk_flag
FROM risk_scenario
ORDER BY scenario;

SELECT 'PROBABILITY COMPONENT GUIDE' AS section;
SELECT model_component, meaning, example, review_question
FROM probability_component_guide
ORDER BY model_component;
