.headers on
.mode column

SELECT 'MOTION ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM motion_assumption_registry
ORDER BY assumption_key;

SELECT 'TRAJECTORY AUDIT CASES' AS section;
SELECT scenario, time_step, point_count, approximate_arc_length, displacement_magnitude, path_efficiency, warning
FROM trajectory_audit_cases
ORDER BY time_step DESC;
