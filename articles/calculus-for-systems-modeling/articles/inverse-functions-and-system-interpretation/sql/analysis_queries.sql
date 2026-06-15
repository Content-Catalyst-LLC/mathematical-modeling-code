.headers on
.mode column

SELECT 'INVERSE MODEL ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM inverse_model_assumption_registry
ORDER BY assumption_key;
