.headers on
.mode column

SELECT 'SURFACE INTEGRAL ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM surface_integral_assumption_registry
ORDER BY assumption_key;

SELECT 'SURFACE INTEGRAL AUDIT CASES' AS section;
SELECT scenario, grid_step, patch_count, approximate_surface_area, scalar_surface_integral, vector_flux_integral, average_flux_density, warning
FROM surface_integral_audit_cases
ORDER BY grid_step DESC;
