.headers on
.mode column
SELECT 'INVERSE RECOVERY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM inverse_recovery_assumption_registry
ORDER BY assumption_key;
SELECT 'INVERSE RECOVERY AUDIT CASES' AS section;
SELECT system_name, matrix_size, determinant, invertible, rank, nullity, recovered_solution, residual_norm, tolerance, warning
FROM inverse_recovery_audit_cases
ORDER BY system_name;
