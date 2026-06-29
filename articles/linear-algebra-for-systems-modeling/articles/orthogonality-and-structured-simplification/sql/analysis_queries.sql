.headers on
.mode column

SELECT 'ORTHOGONALITY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM orthogonality_assumption_registry
ORDER BY assumption_key;

SELECT 'ORTHOGONALITY AUDIT CASES' AS section;
SELECT system_name, dot_product, orthogonal_under_tolerance, residual_norm, orthonormality_error, warning
FROM orthogonality_audit_cases
ORDER BY system_name;
