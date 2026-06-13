.headers on
.mode column

SELECT 'GENERALIZATION LAYERS' AS section;
SELECT generalization_layer, description, typical_failure
FROM generalization_layer_type
ORDER BY generalization_layer;

SELECT 'GENERALIZATION RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, generalization_layer, review_question
FROM generalization_register
WHERE status IN ('review', 'revise');

SELECT 'MODEL GENERALIZATION DIAGNOSTICS' AS section;
SELECT
  model_id,
  model_family,
  training_rmse,
  validation_rmse,
  ROUND(validation_rmse - training_rmse, 4) AS overfit_gap,
  parameter_count,
  ROUND(validation_rmse + 0.20 * complexity_score + 0.08 * parameter_count - 0.20 * interpretability_score, 4) AS generalization_score,
  CASE
    WHEN training_rmse >= 3.0 AND validation_rmse >= 3.0 THEN 'likely_underfit'
    WHEN validation_rmse - training_rmse >= 1.0 AND training_rmse <= 1.0 THEN 'likely_overfit'
    WHEN validation_rmse <= 1.5 AND validation_rmse - training_rmse <= 0.6 THEN 'generalizes_reasonably'
    ELSE 'requires_review'
  END AS classification
FROM generalization_model
ORDER BY generalization_score ASC;

SELECT 'OVERFIT WARNING MODELS' AS section;
SELECT
  model_id,
  training_rmse,
  validation_rmse,
  ROUND(validation_rmse - training_rmse, 4) AS overfit_gap
FROM generalization_model
WHERE validation_rmse - training_rmse >= 1.0
ORDER BY overfit_gap DESC;

SELECT 'GENERALIZATION COMPONENT GUIDE' AS section;
SELECT generalization_layer, meaning, example, review_question
FROM generalization_component_guide
ORDER BY generalization_layer;
