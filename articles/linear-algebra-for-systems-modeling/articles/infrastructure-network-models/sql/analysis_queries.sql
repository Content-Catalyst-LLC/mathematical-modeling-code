.headers on
.mode column

SELECT 'INFRASTRUCTURE MODELING REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM infrastructure_modeling_registry
ORDER BY assumption_key;

SELECT 'INFRASTRUCTURE NETWORK AUDIT CASES' AS section;
SELECT network_name, node_count, edge_count, layer_count, critical_asset_count, interdependency_edge_count, total_baseline_capacity, disrupted_asset, remaining_capacity_after_disruption, capacity_loss_fraction, warning
FROM infrastructure_network_audit_cases
ORDER BY network_name;
