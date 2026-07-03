node_names <- c("water", "power", "transport", "communications", "health")
A <- matrix(c(0.00,0.75,0.20,0.10,0.30, 0.15,0.00,0.65,0.80,0.55, 0.10,0.25,0.00,0.35,0.40, 0.05,0.45,0.30,0.00,0.25, 0.20,0.30,0.35,0.40,0.00), nrow=5, byrow=TRUE)
rownames(A) <- node_names; colnames(A) <- node_names
edge_count <- sum(A != 0); node_count <- nrow(A); density <- edge_count/(node_count*node_count)
A2 <- A %*% A
row_normalize <- function(M){ totals <- rowSums(M); P <- M; for(i in seq_len(nrow(M))){ if(totals[i] > 0){P[i,] <- M[i,]/totals[i]} else {P[i,] <- 0} }; P }
P <- row_normalize(A)
audit_record <- data.frame(network_name="synthetic_infrastructure_dependency_network", node_count=node_count, edge_count=edge_count, directed=TRUE, weighted=TRUE, density=density, max_out_weight=max(rowSums(A)), max_in_weight=max(colSums(A)), two_step_walk_total=sum(A2), row_normalized=TRUE, direction_convention="A[i,j] means dependency or influence from row node i to column node j.", weight_meaning="Synthetic edge weights represent relative dependency strength, not physical capacity.", interpretation_warning="Adjacency conclusions depend on node boundaries, edge definitions, direction conventions, weight meaning, missing-edge assumptions, time variation, and data provenance.")
dir.create("outputs/tables", recursive=TRUE, showWarnings=FALSE)
write.csv(audit_record, "outputs/tables/r_network_adjacency_audit.csv", row.names=FALSE)
write.csv(A, "outputs/tables/r_adjacency_matrix.csv")
write.csv(A2, "outputs/tables/r_two_step_walk_matrix.csv")
write.csv(P, "outputs/tables/r_row_normalized_transition_matrix.csv")
print(audit_record)
