.headers on
.mode column

SELECT 'NETWORK FLOW REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM network_flow_registry
ORDER BY assumption_key;

SELECT 'NETWORK FLOW AUDIT CASES' AS section;
SELECT graph_name, node_count, edge_count, source_node, sink_node, total_source_outflow, total_sink_inflow, capacity_violations, saturated_edge_count, total_flow_cost, warning
FROM network_flow_audit_cases
ORDER BY graph_name;
