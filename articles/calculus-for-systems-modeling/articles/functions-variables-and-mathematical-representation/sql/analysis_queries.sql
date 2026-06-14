.headers on
.mode column

SELECT 'FUNCTIONAL MODEL REGISTRY' AS section;
SELECT model_key, model_name, functional_form, primary_variable, output_variable, interpretation
FROM functional_model_registry
ORDER BY model_key;

SELECT 'MODEL PARAMETERS' AS section;
SELECT model_key, parameter_name, parameter_value, unit, interpretation
FROM model_parameter
ORDER BY model_key, parameter_name;

SELECT 'PARAMETER COUNT BY MODEL' AS section;
SELECT r.model_key, r.model_name, COUNT(p.parameter_name) AS parameter_count
FROM functional_model_registry r
LEFT JOIN model_parameter p ON r.model_key = p.model_key
GROUP BY r.model_key, r.model_name
ORDER BY r.model_key;
