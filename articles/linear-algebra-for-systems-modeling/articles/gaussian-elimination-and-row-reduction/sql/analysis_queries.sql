.headers on
.mode column

SELECT 'ROW REDUCTION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM row_reduction_assumption_registry
ORDER BY assumption_key;

SELECT 'ROW REDUCTION AUDIT CASES' AS section;
SELECT system_name, equation_count, unknown_count, pivot_columns, coefficient_rank, augmented_rank, consistent, solution_behavior, tolerance, warning
FROM row_reduction_audit_cases
ORDER BY system_name;
