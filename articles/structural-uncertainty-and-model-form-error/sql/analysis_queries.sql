.headers on
.mode column

SELECT 'STRUCTURAL LAYERS' AS section;
SELECT structural_layer, description, typical_failure
FROM structural_layer_type
ORDER BY structural_layer;

SELECT 'STRUCTURAL RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, structural_layer, review_question
FROM structural_uncertainty_register
WHERE status IN ('review', 'revise');

SELECT 'PLAUSIBLE MODEL FORMS' AS section;
SELECT model_key, model_family, structural_assumption, review_question
FROM model_form
ORDER BY model_key;

SELECT 'HIGH-PRIORITY STRUCTURAL REVIEW TARGETS' AS section;
SELECT record_key, structural_layer, modeling_role, review_question
FROM structural_uncertainty_register
WHERE structural_layer IN ('model_family', 'relationship', 'boundary', 'aggregation', 'regime');

SELECT 'STRUCTURAL COMPONENT GUIDE' AS section;
SELECT structural_layer, meaning, example, review_question
FROM structural_component_guide
ORDER BY structural_layer;
