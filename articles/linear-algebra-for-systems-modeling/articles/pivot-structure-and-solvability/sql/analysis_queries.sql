.headers on
.mode column

SELECT 'PIVOT STRUCTURE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM pivot_structure_assumption_registry
ORDER BY assumption_key;

SELECT 'PIVOT STRUCTURE AUDIT CASES' AS section;
SELECT system_name, equation_count, unknown_count, pivot_columns, free_columns, coefficient_rank, augmented_rank, consistent, solution_behavior, tolerance, warning
FROM pivot_structure_audit_cases
ORDER BY system_name;
