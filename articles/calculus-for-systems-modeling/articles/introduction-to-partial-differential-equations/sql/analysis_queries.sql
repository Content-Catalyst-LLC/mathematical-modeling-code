.headers on
.mode column

SELECT 'PDE ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM pde_assumption_registry
ORDER BY assumption_key;

SELECT 'PDE AUDIT CASES' AS section;
SELECT scenario, grid_points, diffusivity, dx, dt, steps, stability_ratio, warning
FROM pde_audit_cases
ORDER BY scenario;
