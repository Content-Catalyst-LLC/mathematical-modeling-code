.headers on
.mode column

SELECT 'MATRIX ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM matrix_assumption_registry
ORDER BY assumption_key;

SELECT 'MATRIX STRUCTURE AUDIT CASES' AS section;
SELECT matrix_name, matrix_role, row_count, column_count, nonzero_entries, sparsity_ratio, symmetric, rank_value, warning
FROM matrix_structure_audit_cases
ORDER BY matrix_name;
