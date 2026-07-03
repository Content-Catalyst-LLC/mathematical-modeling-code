.headers on
.mode column

SELECT 'INCIDENCE REPRESENTATION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM incidence_representation_registry
ORDER BY assumption_key;

SELECT 'INCIDENCE STRUCTURE AUDIT CASES' AS section;
SELECT graph_name, node_count, edge_count, incidence_density, max_absolute_node_balance, laplacian_trace, rank_estimate, warning
FROM incidence_structure_audit_cases
ORDER BY graph_name;
