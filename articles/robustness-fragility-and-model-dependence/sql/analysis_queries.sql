.headers on
.mode column

SELECT 'DEPENDENCE LAYERS' AS section;
SELECT dependence_layer, description, typical_failure
FROM dependence_layer_type
ORDER BY dependence_layer;

SELECT 'ROBUSTNESS RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, dependence_layer, review_question
FROM robustness_register
WHERE status IN ('review', 'revise');

SELECT 'ROBUSTNESS SCENARIO MATRIX' AS section;
SELECT scenario_key, model_form, scenario, extraction_multiplier, shock, review_question
FROM robustness_scenario
ORDER BY scenario_key;

SELECT 'HIGH-PRIORITY DEPENDENCE TARGETS' AS section;
SELECT record_key, dependence_layer, modeling_role, review_question
FROM robustness_register
WHERE dependence_layer IN ('model_form', 'scenario', 'decision_threshold', 'data');

SELECT 'DEPENDENCE COMPONENT GUIDE' AS section;
SELECT dependence_layer, meaning, example, review_question
FROM dependence_component_guide
ORDER BY dependence_layer;
