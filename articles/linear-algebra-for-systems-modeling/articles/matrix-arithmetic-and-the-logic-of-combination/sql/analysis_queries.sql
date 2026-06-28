.headers on
.mode column

SELECT 'MATRIX ARITHMETIC ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM matrix_arithmetic_assumption_registry
ORDER BY assumption_key;

SELECT 'MATRIX ARITHMETIC AUDIT CASES' AS section;
SELECT operation_name, matrix_shape, compatible_shape, output_entry_sum, warning
FROM matrix_arithmetic_audit_cases
ORDER BY operation_name;
