.headers on
.mode column

SELECT 'UNCERTAINTY LAYERS' AS section;
SELECT uncertainty_layer, description, typical_failure
FROM uncertainty_layer_type
ORDER BY uncertainty_layer;

SELECT 'UNCERTAINTY RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, uncertainty_layer, review_question
FROM uncertainty_register
WHERE status IN ('review', 'revise');

SELECT 'UNCERTAIN PARAMETER RANGE REVIEW' AS section;
SELECT
  parameter_name,
  uncertainty_type,
  baseline,
  low,
  high,
  ROUND(high - low, 6) AS range_width,
  ROUND((high - low) / NULLIF(ABS(baseline), 0), 6) AS relative_range,
  description
FROM uncertain_parameter
ORDER BY relative_range DESC;

SELECT 'STRUCTURAL AND DECISION UNCERTAINTY TARGETS' AS section;
SELECT record_key, uncertainty_layer, modeling_role, review_question
FROM uncertainty_register
WHERE uncertainty_layer IN ('model_form', 'decision_support', 'scenario');

SELECT 'UNCERTAINTY COMPONENT GUIDE' AS section;
SELECT uncertainty_layer, meaning, example, review_question
FROM uncertainty_component_guide
ORDER BY uncertainty_layer;
