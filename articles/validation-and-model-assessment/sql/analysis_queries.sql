.headers on
.mode column

SELECT 'VALIDATION LAYERS' AS section;
SELECT validation_layer, description, typical_failure
FROM validation_layer_type
ORDER BY validation_layer;

SELECT 'VALIDATION RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, validation_layer, assessment_question
FROM validation_register
WHERE status IN ('review', 'revise');

SELECT 'VALIDATION ERROR DIAGNOSTICS' AS section;
SELECT
  time,
  scenario,
  observed_value,
  predicted_value,
  ROUND(observed_value - predicted_value, 4) AS residual,
  ROUND(ABS(observed_value - predicted_value), 4) AS absolute_error
FROM validation_observation
ORDER BY time;

SELECT 'SCENARIO ERROR SUMMARY' AS section;
SELECT
  scenario,
  ROUND(AVG(ABS(observed_value - predicted_value)), 4) AS mae,
  ROUND(SQRT(AVG((observed_value - predicted_value) * (observed_value - predicted_value))), 4) AS rmse,
  COUNT(*) AS n
FROM validation_observation
GROUP BY scenario
ORDER BY scenario;

SELECT 'VALIDATION COMPONENT GUIDE' AS section;
SELECT validation_layer, meaning, example, review_question
FROM validation_component_guide
ORDER BY validation_layer;
