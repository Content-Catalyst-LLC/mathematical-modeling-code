.headers on
.mode column

SELECT 'CONSTRAINED OPTIMIZATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM constrained_optimization_assumption_registry
ORDER BY assumption_key;

SELECT 'CONSTRAINED OPTIMIZATION CASES' AS section;
SELECT x, y, objective_value, constraint_target, lambda_value, stationarity_residual_norm, feasible, warning
FROM constrained_optimization_cases
ORDER BY constraint_target;
