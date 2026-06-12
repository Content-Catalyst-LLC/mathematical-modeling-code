# Base R workflow for network review and connectivity diagnostics.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

tables_dir <- file.path(article_root, "outputs", "tables")
figures_dir <- file.path(article_root, "outputs", "figures")
dir.create(tables_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

node_path <- file.path(tables_dir, "network_node_diagnostics.csv")
edge_path <- file.path(tables_dir, "network_edge_list.csv")
register_path <- file.path(tables_dir, "network_model_register.csv")

if (!file.exists(node_path) || !file.exists(edge_path)) {
  stop("Missing network outputs. Run make python first.")
}

nodes <- read.csv(node_path, stringsAsFactors = FALSE)
edges <- read.csv(edge_path, stringsAsFactors = FALSE)

nodes$in_degree <- as.numeric(nodes$in_degree)
nodes$out_degree <- as.numeric(nodes$out_degree)
nodes$total_degree <- as.numeric(nodes$total_degree)
nodes$weighted_out_degree <- as.numeric(nodes$weighted_out_degree)
nodes$reachable_nodes <- as.numeric(nodes$reachable_nodes)

median_reach <- median(nodes$reachable_nodes, na.rm = TRUE)
median_weighted_out <- median(nodes$weighted_out_degree, na.rm = TRUE)

nodes$structural_review <- ifelse(
  nodes$reachable_nodes >= median_reach & nodes$weighted_out_degree >= median_weighted_out,
  "high structural review priority",
  ifelse(nodes$in_degree + nodes$out_degree == 0, "isolated node review", "routine review")
)

write.csv(nodes, file.path(tables_dir, "r_network_node_review_summary.csv"), row.names = FALSE)

edge_quality <- as.data.frame(table(edges$evidence_quality), stringsAsFactors = FALSE)
names(edge_quality) <- c("evidence_quality", "edge_count")
write.csv(edge_quality, file.path(tables_dir, "r_network_edge_evidence_summary.csv"), row.names = FALSE)

if (file.exists(register_path)) {
  register <- read.csv(register_path, stringsAsFactors = FALSE)
  register$priority <- ifelse(register$network_risk_score >= 8, "high", ifelse(register$network_risk_score >= 6, "medium", "low"))
  write.csv(register, file.path(tables_dir, "r_network_model_review_queue.csv"), row.names = FALSE)
}

png(file.path(figures_dir, "r_network_degree_diagnostics.png"), width = 1100, height = 720)

degree_total <- nodes$in_degree + nodes$out_degree
names(degree_total) <- nodes$node

if (length(degree_total) > 0 && any(is.finite(degree_total))) {
  barplot(sort(degree_total, decreasing = TRUE), las = 2, ylab = "Total degree", main = "Network Node Degree Diagnostics")
  grid()
} else {
  plot.new()
  title(main = "Network Node Degree Diagnostics")
  text(0.5, 0.5, "No finite degree values available.")
}

dev.off()

print(nodes)
