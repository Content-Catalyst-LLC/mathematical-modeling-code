.headers on
.mode column

SELECT 'NETWORK INFLUENCE REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM network_influence_registry
ORDER BY assumption_key;

SELECT 'PAGERANK AUDIT CASES' AS section;
SELECT graph_name, node_count, edge_count, damping_factor, tolerance, converged, rank_sum, dangling_node_count, warning
FROM pagerank_audit_cases
ORDER BY graph_name;
