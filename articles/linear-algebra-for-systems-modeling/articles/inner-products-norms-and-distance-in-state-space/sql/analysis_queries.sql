.headers on
.mode column

SELECT 'STATE SPACE GEOMETRY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM state_space_geometry_assumption_registry
ORDER BY assumption_key;

SELECT 'STATE SPACE GEOMETRY AUDIT CASES' AS section;
SELECT system_name, norm_1, norm_2, norm_inf, euclidean_distance, weighted_distance, warning
FROM state_space_geometry_audit_cases
ORDER BY system_name;
