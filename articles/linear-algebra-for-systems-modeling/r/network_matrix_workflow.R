# Linear Algebra for Systems Modeling:
# Network adjacency matrix workflow in R.
# Educational example only.

library(tidyverse)

edges <- read_csv("../data/network_edges.csv", show_col_types = FALSE)

nodes <- sort(unique(c(edges$source, edges$target)))

adjacency <- matrix(0, nrow = length(nodes), ncol = length(nodes))
rownames(adjacency) <- nodes
colnames(adjacency) <- nodes

for (i in seq_len(nrow(edges))) {
  adjacency[edges$source[i], edges$target[i]] <- edges$weight[i]
}

network_summary <- tibble(
  node = nodes,
  out_strength = rowSums(adjacency),
  in_strength = colSums(adjacency)
)

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(as_tibble(adjacency, rownames = "node"), "../outputs/r_adjacency_matrix.csv")
write_csv(network_summary, "../outputs/r_network_summary.csv")

print(network_summary)
