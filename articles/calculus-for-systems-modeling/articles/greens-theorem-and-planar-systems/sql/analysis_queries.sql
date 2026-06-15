.headers on
.mode column

SELECT 'GREENS THEOREM ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM greens_theorem_assumption_registry
ORDER BY assumption_key;

SELECT 'GREENS THEOREM AUDIT CASES' AS section;
SELECT scenario, boundary_segments_per_side, interior_grid_step, boundary_circulation, interior_curl_integral, boundary_flux, interior_divergence_integral, circulation_gap, flux_gap, warning
FROM greens_theorem_audit_cases
ORDER BY boundary_segments_per_side;
