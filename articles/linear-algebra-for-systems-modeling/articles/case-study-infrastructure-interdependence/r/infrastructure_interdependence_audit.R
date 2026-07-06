sectors <- c("power", "water", "communications", "transportation", "health")

dependency <- matrix(
  c(
    0.00, 0.05, 0.10, 0.10, 0.00,
    0.70, 0.00, 0.10, 0.20, 0.00,
    0.60, 0.00, 0.00, 0.10, 0.00,
    0.30, 0.00, 0.20, 0.00, 0.05,
    0.80, 0.50, 0.40, 0.30, 0.00
  ),
  nrow = length(sectors),
  byrow = TRUE
)

rownames(dependency) <- sectors
colnames(dependency) <- sectors

initial_disruption <- rep(0, length(sectors))
names(initial_disruption) <- sectors
initial_disruption["power"] <- 0.40

downstream_loss <- dependency %*% initial_disruption
dependency_burden <- colSums(dependency)

audit_record <- data.frame(
  workflow_name = "infrastructure_interdependence_audit",
  scenario_name = "synthetic_power_disruption_dependency_scenario",
  sector_count = length(sectors),
  initial_shock_sector = "power",
  initial_shock_magnitude = 0.40,
  highest_dependency_burden_sector = names(which.max(dependency_burden)),
  highest_dependency_burden = max(dependency_burden),
  largest_downstream_loss_sector = rownames(downstream_loss)[which.max(downstream_loss)],
  largest_downstream_loss = max(downstream_loss),
  total_estimated_downstream_loss = sum(downstream_loss),
  sensitivity_warning = paste(
    "Dependency weights are scenario assumptions.",
    "Results should be compared across alternative weights, redundancy assumptions,",
    "time delays, and recovery capacities."
  ),
  interpretation_warning = paste(
    "This one-step linear cascade estimate supports exploratory planning only.",
    "It does not predict real failure behavior without geography, capacity, timing,",
    "backup systems, operational response, validation evidence, and equity review."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_infrastructure_interdependence_audit.csv", row.names = FALSE)
print(audit_record)
