.headers on
.mode column

SELECT 'LINEAR SYSTEM ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM linear_system_assumption_registry
ORDER BY assumption_key;

SELECT 'LINEAR SYSTEM AUDIT CASES' AS section;
SELECT system_name, equation_count, unknown_count, coefficient_rank, augmented_rank, consistent, solution_behavior, warning
FROM linear_system_audit_cases
ORDER BY system_name;
