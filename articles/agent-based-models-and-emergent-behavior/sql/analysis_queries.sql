.headers on
.mode column

SELECT 'ABM COMPONENT TYPES' AS section;
SELECT component_type, description, typical_failure
FROM abm_component_type
ORDER BY component_type;

SELECT 'ABM RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, component_type, rule_or_structure, review_question
FROM abm_model_register
WHERE status IN ('review', 'revise');

SELECT 'ABM SCENARIOS' AS section;
SELECT scenario, agent_count, initial_adopters, adoption_threshold_low, adoption_threshold_high, steps, replications
FROM abm_scenario
ORDER BY scenario;

SELECT 'SCENARIO INTENSITY CHECK' AS section;
SELECT
  scenario,
  ROUND(1.0 * initial_adopters / agent_count, 3) AS initial_adoption_share,
  ROUND((adoption_threshold_low + adoption_threshold_high) / 2.0, 3) AS mean_threshold,
  replications
FROM abm_scenario
ORDER BY mean_threshold;

SELECT 'ABM COMPONENT GUIDE' AS section;
SELECT component_type, meaning, example, review_question
FROM abm_component_guide
ORDER BY component_type;
