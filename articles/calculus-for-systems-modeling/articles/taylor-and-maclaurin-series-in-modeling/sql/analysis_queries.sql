.headers on
.mode column

SELECT 'TAYLOR APPROXIMATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM taylor_approximation_assumption_registry
ORDER BY assumption_key;

SELECT 'TAYLOR APPROXIMATION CASES' AS section;
SELECT function_name, center, x_value, approximation_order, review_warning
FROM taylor_approximation_cases
ORDER BY function_name, x_value;
