.headers on
.mode column

SELECT 'SELECTION LAYERS' AS section;
SELECT selection_layer, description, typical_failure
FROM selection_layer_type
ORDER BY selection_layer;

SELECT 'SELECTION RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, selection_layer, review_question
FROM model_selection_register
WHERE status IN ('review', 'revise');

SELECT 'MODEL COMPARISON RANKING' AS section;
SELECT
  model_id,
  model_family,
  calibration_rmse,
  validation_rmse,
  ROUND(validation_rmse - calibration_rmse, 4) AS overfit_gap,
  parameter_count,
  ROUND(validation_rmse + 0.08 * parameter_count - 0.35 * interpretability_score - 0.40 * robustness_score - 0.35 * decision_relevance_score, 4) AS comparison_score
FROM model_candidate
ORDER BY comparison_score ASC;

SELECT 'OVERFIT WARNING MODELS' AS section;
SELECT
  model_id,
  calibration_rmse,
  validation_rmse,
  ROUND(validation_rmse - calibration_rmse, 4) AS overfit_gap
FROM model_candidate
WHERE validation_rmse - calibration_rmse > 1.0
ORDER BY overfit_gap DESC;

SELECT 'SELECTION CRITERIA' AS section;
SELECT criterion, meaning, selection_role, risk_if_ignored
FROM selection_criteria
ORDER BY criterion;
