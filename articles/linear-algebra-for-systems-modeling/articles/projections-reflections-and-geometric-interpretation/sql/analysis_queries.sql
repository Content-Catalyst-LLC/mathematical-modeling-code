.headers on
.mode column

SELECT 'GEOMETRIC TRANSFORMATION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM geometric_transformation_assumption_registry
ORDER BY assumption_key;

SELECT 'PROJECTION REFLECTION AUDIT CASES' AS section;
SELECT system_name, residual_norm, projection_idempotence_error, projection_symmetry_error, reflection_involution_error, length_preservation_error, warning
FROM projection_reflection_audit_cases
ORDER BY system_name;
