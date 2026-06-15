records <- data.frame(
  step = 1:5,
  duration = c(1, 1, 1, 1, 1),
  inflow = c(12, 10, 9, 8, 7),
  outflow = c(6, 7, 8, 9, 9),
  exposure_intensity = c(20, 18, 15, 13, 11),
  population_weight = c(1000, 1100, 1050, 980, 960)
)

initial_stock <- 50

cumulative_inflow <- sum(records$inflow * records$duration)
cumulative_outflow <- sum(records$outflow * records$duration)
net_accumulation <- cumulative_inflow - cumulative_outflow
ending_stock <- initial_stock + net_accumulation
gross_activity <- cumulative_inflow + cumulative_outflow

cumulative_exposure <- sum(records$exposure_intensity * records$duration)
population_weighted_exposure <- sum(
  records$exposure_intensity *
    records$population_weight *
    records$duration
)

warning <- ""
if (ending_stock < 0) {
  warning <- "ending stock is negative; check constraints or sign conventions"
}

audit <- data.frame(
  initial_stock = initial_stock,
  cumulative_inflow = cumulative_inflow,
  cumulative_outflow = cumulative_outflow,
  net_accumulation = net_accumulation,
  ending_stock = ending_stock,
  cumulative_exposure = cumulative_exposure,
  population_weighted_exposure = population_weighted_exposure,
  gross_activity = gross_activity,
  method = "discrete time-step accumulation",
  unit_check = "flow multiplied by duration gives stock units; intensity multiplied by duration gives exposure units",
  warning = warning
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(records, "outputs/tables/r_flow_to_stock_records.csv", row.names = FALSE)
write.csv(audit, "outputs/tables/r_flow_to_stock_audit.csv", row.names = FALSE)

print(audit)
