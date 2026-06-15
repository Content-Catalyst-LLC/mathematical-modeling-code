.headers on
.mode column

SELECT 'DERIVATIVE RATE ASSUMPTION REGISTRY' AS section;
SELECT concept_name, formal_role, systems_modeling_role, review_warning
FROM derivative_rate_assumption_registry
ORDER BY assumption_key;

SELECT 'DERIVATIVE METHOD REGISTRY' AS section;
SELECT method_name, approximation_role, numerical_warning
FROM derivative_method_registry
ORDER BY method_key;

SELECT 'DERIVATIVE WARNING REGISTRY' AS section;
SELECT warning_name, interpretation
FROM derivative_warning_registry
ORDER BY warning_key;
