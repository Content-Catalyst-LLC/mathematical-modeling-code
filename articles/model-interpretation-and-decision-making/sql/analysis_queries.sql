.headers on
.mode column

SELECT 'INTERPRETATION LAYERS' AS section;
SELECT interpretation_layer, description, typical_failure
FROM interpretation_layer_type
ORDER BY interpretation_layer;

SELECT 'INTERPRETATION RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, interpretation_layer, decision_question
FROM interpretation_register
WHERE status IN ('review', 'revise');

SELECT 'DECISION OPTIONS WITH THRESHOLD REVIEW' AS section;
SELECT
  option_key,
  option_name,
  expected_stock,
  lower_bound,
  upper_bound,
  ROUND(expected_stock - 45.0, 3) AS threshold_margin,
  CASE WHEN lower_bound < 45.0 THEN 'fragile' ELSE 'robust' END AS robustness_class,
  ROUND(expected_stock - 0.8 * implementation_burden - 1.2 * consequence_if_wrong - CASE WHEN lower_bound < 45.0 THEN 8.0 ELSE 0.0 END, 3) AS decision_score
FROM decision_option
ORDER BY decision_score DESC;

SELECT 'STAKEHOLDER DECISION GUIDE' AS section;
SELECT stakeholder_group, decision_concern, interpretation_need, governance_question
FROM stakeholder_decision_guide
ORDER BY stakeholder_group;

SELECT 'GOVERNANCE REVIEW TARGETS' AS section;
SELECT record_key, interpretation_layer, model_role, decision_question
FROM interpretation_register
WHERE interpretation_layer IN ('decision_threshold', 'values', 'governance');
