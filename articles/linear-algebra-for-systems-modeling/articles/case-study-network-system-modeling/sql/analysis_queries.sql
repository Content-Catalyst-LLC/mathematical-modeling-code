.headers on
.mode column

SELECT 'NETWORK GOVERNANCE REGISTRY' AS section;
SELECT governance_name, modeling_role, review_requirement, responsible_use_warning
FROM network_modeling_governance_registry
ORDER BY governance_key;

SELECT 'SYNTHETIC NETWORK EDGES' AS section;
SELECT source_node, target_node, weight, edge_meaning
FROM synthetic_network_edges
ORDER BY source_node, target_node;

SELECT 'NETWORK SYSTEM MODELING AUDIT CASES' AS section;
SELECT workflow_name, network_name, node_count, edge_count, total_weight, highest_weighted_degree_node, highest_weighted_degree, laplacian_trace, baseline_component_count, stressed_component_count, removed_edge, vulnerability_warning, interpretation_warning
FROM network_system_modeling_audit_cases
ORDER BY workflow_name;
