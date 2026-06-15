.headers on
.mode column
SELECT 'MULTIVARIABLE FUNCTION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM multivariable_function_assumption_registry
ORDER BY assumption_key;

SELECT 'MULTIVARIABLE FUNCTION CASES' AS section;
SELECT x, y, output, feasible, warning
FROM multivariable_function_cases
ORDER BY x, y;
