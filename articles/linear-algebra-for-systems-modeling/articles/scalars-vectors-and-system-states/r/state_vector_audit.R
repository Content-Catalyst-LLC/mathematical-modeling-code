state_components <- data.frame(
  position = 1:5,
  component_name = c("road_condition", "bridge_condition", "water_reliability", "power_reliability", "transit_capacity"),
  value = c(72.0, 68.0, 0.91, 0.96, 125000.0),
  unit = c("index_0_to_100", "index_0_to_100", "probability", "probability", "daily_passenger_capacity"),
  scale_type = c("raw_index", "raw_index", "proportion", "proportion", "raw_count")
)

raw_norm <- sqrt(sum(state_components$value^2))
state_components$z_score_within_example <- as.numeric(scale(state_components$value))

audit_summary <- data.frame(
  state_name = "infrastructure_condition_state",
  dimension = nrow(state_components),
  raw_euclidean_norm = raw_norm,
  audit_warning = paste("The raw norm is dominated by high-magnitude components.", "Scaling choices should be documented before distance comparisons.")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(state_components, "outputs/tables/r_state_vector_components.csv", row.names = FALSE)
write.csv(audit_summary, "outputs/tables/r_state_vector_summary.csv", row.names = FALSE)
print(state_components)
print(audit_summary)
