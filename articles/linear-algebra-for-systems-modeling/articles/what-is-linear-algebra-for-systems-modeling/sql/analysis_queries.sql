.headers on
.mode column

SELECT 'LINEAR ALGEBRA ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM linear_algebra_assumption_registry
ORDER BY assumption_key;

SELECT 'MATRIX AUDIT CASES' AS section;
SELECT model_name, rows, columns, matrix_meaning, interpretation_warning
FROM matrix_audit_cases
ORDER BY model_name;
