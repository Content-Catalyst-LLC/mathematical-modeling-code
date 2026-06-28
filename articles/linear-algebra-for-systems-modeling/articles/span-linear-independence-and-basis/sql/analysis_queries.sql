.headers on
.mode column

SELECT 'SPAN BASIS ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM span_basis_assumption_registry
ORDER BY assumption_key;

SELECT 'SPAN BASIS AUDIT CASES' AS section;
SELECT vector_set_name, ambient_dimension, vector_count, rank_value, spans_ambient_space, linearly_independent, is_basis_for_ambient_space, warning
FROM span_basis_audit_cases
ORDER BY vector_set_name;
