.headers on
.mode column

SELECT 'RANK NULLITY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM rank_nullity_assumption_registry
ORDER BY assumption_key;

SELECT 'RANK NULLITY AUDIT CASES' AS section;
SELECT system_name, row_count, column_count, rank, nullity, rank_deficient, pivot_columns, free_columns, tolerance, warning
FROM rank_nullity_audit_cases
ORDER BY system_name;
