.headers on
.mode column

SELECT 'POWER SERIES ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM power_series_assumption_registry
ORDER BY assumption_key;

SELECT 'POWER SERIES APPROXIMATION CASES' AS section;
SELECT function_name, center, x_value, n_terms, convergence_status, review_warning
FROM power_series_approximation_cases
ORDER BY x_value, n_terms;
