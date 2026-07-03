sectors <- c("energy", "manufacturing", "transport", "services")

transactions <- matrix(
  c(
    8, 18, 10, 7,
    4, 12, 8, 11,
    3, 9, 6, 8,
    5, 14, 7, 16
  ),
  nrow = 4,
  byrow = TRUE
)

rownames(transactions) <- sectors
colnames(transactions) <- sectors

total_output <- c(80, 120, 90, 140)
final_demand <- c(37, 67, 59, 98)
emissions_intensity <- c(0.72, 0.45, 0.60, 0.18)

A <- sweep(transactions, 2, total_output, FUN = "/")
I <- diag(length(sectors))
net_requirements <- I - A

spectral_radius <- max(Mod(eigen(A)$values))
productive_system_flag <- spectral_radius < 1

leontief_inverse <- solve(net_requirements)
solved_output <- leontief_inverse %*% final_demand
output_multipliers <- colSums(leontief_inverse)

demand_shock <- c(0, 10, 0, 15)
output_change <- leontief_inverse %*% demand_shock
emissions_for_final_demand <- as.numeric(emissions_intensity %*% solved_output)

audit_record <- data.frame(
  model_name = "synthetic_leontief_intersectoral_dependence_audit",
  sectors = length(sectors),
  method = "demand_driven_leontief_system",
  coefficient_basis = "sector_input_per_unit_output",
  spectral_radius = spectral_radius,
  condition_number = kappa(net_requirements),
  productive_system_flag = productive_system_flag,
  maximum_output_multiplier = max(output_multipliers),
  highest_multiplier_sector = sectors[which.max(output_multipliers)],
  total_output_required = sum(solved_output),
  total_shock_output_change = sum(output_change),
  emissions_for_final_demand = emissions_for_final_demand,
  assumption_warning = paste(
    "The Leontief model assumes fixed technical coefficients, proportional production,",
    "no price response, no substitution, and no binding capacity constraints."
  ),
  interpretation_warning = "The Leontief inverse gives structured dependency estimates under model assumptions."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_leontief_system_audit.csv", row.names = FALSE)
write.csv(A, "outputs/tables/r_technical_coefficients.csv")
write.csv(leontief_inverse, "outputs/tables/r_leontief_inverse.csv")
write.csv(data.frame(sector = sectors, output_change = as.numeric(output_change)),
          "outputs/tables/r_shock_output_change.csv",
          row.names = FALSE)
print(audit_record)
