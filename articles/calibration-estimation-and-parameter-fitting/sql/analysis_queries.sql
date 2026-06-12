.headers on
.mode column

SELECT 'CALIBRATION LAYERS' AS section;
SELECT calibration_layer, description, typical_failure
FROM calibration_layer_type
ORDER BY calibration_layer;

SELECT 'CALIBRATION RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, calibration_layer, diagnostic_question
FROM calibration_register
WHERE status IN ('review', 'revise');

SELECT 'CALIBRATION OBSERVATIONS' AS section;
SELECT time, observed_stock, extraction
FROM calibration_observation
ORDER BY time;

SELECT 'PARAMETER GRID' AS section;
SELECT growth_rate_min, growth_rate_max, growth_rate_step, carrying_capacity_min, carrying_capacity_max, carrying_capacity_step
FROM parameter_grid;

SELECT 'CALIBRATION COMPONENT GUIDE' AS section;
SELECT calibration_layer, meaning, example, review_question
FROM calibration_component_guide
ORDER BY calibration_layer;
