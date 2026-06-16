.headers on
.mode column

SELECT 'SYMBOLIC MODEL INSPECTION REGISTRY' AS section;
SELECT inspection_name, symbolic_operation, systems_modeling_role, review_warning
FROM symbolic_model_inspection_registry
ORDER BY inspection_key;

SELECT 'SYMBOLIC EXPRESSION RECORDS' AS section;
SELECT item, expression, interpretation, warning
FROM symbolic_expression_records
ORDER BY item;
