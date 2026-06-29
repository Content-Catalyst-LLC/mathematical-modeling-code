.headers on
.mode column

SELECT 'CHANGE OF BASIS ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM change_of_basis_assumption_registry
ORDER BY assumption_key;

SELECT 'CHANGE OF BASIS AUDIT CASES' AS section;
SELECT system_name, basis_shape, basis_rank, basis_determinant, basis_coordinates, reconstruction_error, warning
FROM change_of_basis_audit_cases
ORDER BY system_name;
