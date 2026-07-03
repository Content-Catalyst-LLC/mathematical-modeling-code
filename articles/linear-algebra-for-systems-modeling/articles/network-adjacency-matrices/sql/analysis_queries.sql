.headers on
.mode column
SELECT 'NETWORK ADJACENCY ASSUMPTION REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning FROM network_adjacency_assumption_registry ORDER BY assumption_key;
SELECT 'NETWORK ADJACENCY AUDIT CASES' AS section;
SELECT network_name, node_count, edge_count, density, max_out_weight, max_in_weight, warning FROM network_adjacency_audit_cases ORDER BY network_name;
