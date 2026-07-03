result <- data.frame(calculator="network_adjacency_calculator", network_name="synthetic_infrastructure_dependency_network", node_count=5, edge_count=20, directed=TRUE, weighted=TRUE, density=0.8, max_out_weight=2.15, max_in_weight=1.95, row_normalized=TRUE, warning="Adjacency metrics depend on node boundaries, edge definitions, direction conventions, weight meaning, and data provenance.")
dir.create("outputs", recursive=TRUE, showWarnings=FALSE)
write.csv(result, "outputs/r_network_adjacency_calculator.csv", row.names=FALSE)
print(result)
