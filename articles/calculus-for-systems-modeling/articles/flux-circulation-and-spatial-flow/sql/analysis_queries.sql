.headers on
.mode column

SELECT 'FLOW ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM flow_assumption_registry
ORDER BY assumption_key;

SELECT 'FLOW AUDIT CASES' AS section;
SELECT scenario, segment_count, approximate_flux, approximate_circulation, mean_tangential_alignment, mean_normal_alignment, warning
FROM flow_audit_cases
ORDER BY segment_count;
