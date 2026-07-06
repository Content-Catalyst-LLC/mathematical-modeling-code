sectors <- c("agriculture", "manufacturing", "services")

A <- matrix(
  c(
    0.10, 0.20, 0.05,
    0.15, 0.25, 0.10,
    0.05, 0.10, 0.20
  ),
  nrow = length(sectors),
  byrow = TRUE
)

rownames(A) <- sectors
colnames(A) <- sectors

final_demand <- c(100.0, 150.0, 200.0)
names(final_demand) <- sectors

I <- diag(length(sectors))
leontief_matrix <- I - A
total_requirements <- solve(leontief_matrix)
gross_output <- total_requirements %*% final_demand

multipliers <- colSums(total_requirements)

demand_shock <- c(0.0, 25.0, 0.0)
names(demand_shock) <- sectors
output_change <- total_requirements %*% demand_shock

condition_estimate <- norm(leontief_matrix, type = "I") * norm(total_requirements, type = "I")

audit_record <- data.frame(
  workflow_name = "economic_input_output_audit",
  economy_name = "synthetic_three_sector_economy",
  sector_count = length(sectors),
  final_demand_total = sum(final_demand),
  gross_output_total = sum(gross_output),
  highest_multiplier_sector = names(which.max(multipliers)),
  highest_output_multiplier = max(multipliers),
  shock_sector = "manufacturing",
  shock_amount = 25.0,
  gross_output_change_total = sum(output_change),
  leontief_infinity_condition_estimate = condition_estimate,
  solvability_warning = paste(
    "The Leontief matrix must be invertible and the solution should be checked",
    "for numerical stability, residual error, plausibility, and economically meaningful output levels."
  ),
  interpretation_warning = paste(
    "Input-output results depend on fixed technical coefficients, sector aggregation,",
    "domestic/import boundaries, price basis, final-demand assumptions, and capacity limits.",
    "Multipliers are not automatic measures of welfare, productivity, or policy priority."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_economic_input_output_audit.csv", row.names = FALSE)
print(audit_record)
