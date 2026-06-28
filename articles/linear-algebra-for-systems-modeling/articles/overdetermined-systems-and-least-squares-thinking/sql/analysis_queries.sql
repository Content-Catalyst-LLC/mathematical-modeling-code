.headers on
.mode column

SELECT 'LEAST SQUARES ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM least_squares_assumption_registry
ORDER BY assumption_key;

SELECT 'LEAST SQUARES AUDIT CASES' AS section;
SELECT system_name, row_count, column_count, overdetermined, rank, solution, residual_norm, solver_method, warning
FROM least_squares_audit_cases
ORDER BY system_name;
