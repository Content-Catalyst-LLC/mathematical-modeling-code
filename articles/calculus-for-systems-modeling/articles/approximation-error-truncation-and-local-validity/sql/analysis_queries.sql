.headers on
.mode column

SELECT 'APPROXIMATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM approximation_assumption_registry
ORDER BY assumption_key;

SELECT 'APPROXIMATION ERROR CASES' AS section;
SELECT method, function_name, center, x_value, approximation_order, warning
FROM approximation_error_cases
ORDER BY function_name, x_value;
