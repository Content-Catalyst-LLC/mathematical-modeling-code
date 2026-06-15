.headers on
.mode column

SELECT 'STOKES THEOREM ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM stokes_theorem_assumption_registry
ORDER BY assumption_key;

SELECT 'STOKES THEOREM AUDIT CASES' AS section;
SELECT scenario, radius, boundary_segments, radial_steps, boundary_circulation, surface_curl_flux, absolute_gap, orientation_note, warning
FROM stokes_theorem_audit_cases
ORDER BY boundary_segments;
