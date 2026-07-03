.headers on
.mode column

SELECT 'GRAPH MODELING REGISTRY' AS section;
SELECT assumption_name, mathematical_role, systems_modeling_role, review_warning
FROM graph_modeling_registry
ORDER BY assumption_key;

SELECT 'GRAPH STRUCTURE AUDIT CASES' AS section;
SELECT graph_name, node_count, edge_count, component_count, max_degree, min_degree, average_degree, graph_density, warning
FROM graph_structure_audit_cases
ORDER BY graph_name;
