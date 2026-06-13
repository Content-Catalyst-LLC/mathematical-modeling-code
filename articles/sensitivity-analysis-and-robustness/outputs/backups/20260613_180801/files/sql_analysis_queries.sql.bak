.headers on
.mode column

SELECT 'SENSITIVITY LAYERS' AS section;
SELECT sensitivity_layer, description, typical_failure
FROM sensitivity_layer_type
ORDER BY sensitivity_layer;

SELECT 'SENSITIVITY RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, sensitivity_layer, review_question
FROM sensitivity_register
WHERE status IN ('review', 'revise');

SELECT 'PARAMETER RANGE REVIEW' AS section;
SELECT
  parameter_name,
  uncertainty_label,
  baseline,
  low,
  high,
  ROUND(high - low, 6) AS range_width,
  ROUND((high - low) / NULLIF(ABS(baseline), 0), 6) AS relative_range
FROM sensitivity_parameter
ORDER BY relative_range DESC;

SELECT 'HIGH-UNCERTAINTY REVIEW TARGETS' AS section;
SELECT
  parameter_name,
  uncertainty_label,
  ROUND((high - low) / NULLIF(ABS(baseline), 0), 6) AS relative_range
FROM sensitivity_parameter
WHERE uncertainty_label IN ('policy','scenario','structural')
ORDER BY relative_range DESC;

SELECT 'SENSITIVITY COMPONENT GUIDE' AS section;
SELECT sensitivity_layer, meaning, example, review_question
FROM sensitivity_component_guide
ORDER BY sensitivity_layer;
