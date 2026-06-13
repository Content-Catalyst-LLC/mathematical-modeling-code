.headers on
.mode column

SELECT 'DIAGNOSTIC LAYERS' AS section;
SELECT diagnostic_layer, description, typical_failure
FROM diagnostic_layer_type
ORDER BY diagnostic_layer;

SELECT 'DIAGNOSTIC RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, diagnostic_layer, review_question
FROM diagnostic_register
WHERE status IN ('review', 'revise');

SELECT 'RESIDUAL DIAGNOSTICS' AS section;
SELECT
  time,
  diagnostic_group,
  observed_value,
  predicted_value,
  ROUND(observed_value - predicted_value, 4) AS residual,
  ROUND(ABS(observed_value - predicted_value), 4) AS absolute_error,
  CASE
    WHEN ABS(observed_value - decision_threshold) <= 3.0 THEN 'near_threshold'
    ELSE 'not_near_threshold'
  END AS threshold_flag,
  CASE
    WHEN (observed_value < decision_threshold) != (predicted_value < decision_threshold) THEN 'decision_disagreement'
    ELSE 'agreement'
  END AS decision_status
FROM diagnostic_observation
ORDER BY time;

SELECT 'GROUP ERROR SUMMARY' AS section;
SELECT
  diagnostic_group,
  ROUND(AVG(observed_value - predicted_value), 4) AS mean_error,
  ROUND(AVG(ABS(observed_value - predicted_value)), 4) AS mae,
  ROUND(SQRT(AVG((observed_value - predicted_value) * (observed_value - predicted_value))), 4) AS rmse,
  COUNT(*) AS n
FROM diagnostic_observation
GROUP BY diagnostic_group
ORDER BY diagnostic_group;

SELECT 'DIAGNOSTIC COMPONENT GUIDE' AS section;
SELECT diagnostic_layer, meaning, example, review_question
FROM diagnostic_component_guide
ORDER BY diagnostic_layer;
