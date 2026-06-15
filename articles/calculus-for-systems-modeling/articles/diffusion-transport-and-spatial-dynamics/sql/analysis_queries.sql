.headers on
.mode column

SELECT 'SPATIAL DYNAMICS ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM spatial_dynamics_assumption_registry
ORDER BY assumption_key;

SELECT 'SPATIAL AUDIT CASES' AS section;
SELECT scenario, grid_points, diffusivity, velocity, dx, dt, steps, diffusion_ratio, transport_ratio, warning
FROM spatial_audit_cases
ORDER BY scenario;
