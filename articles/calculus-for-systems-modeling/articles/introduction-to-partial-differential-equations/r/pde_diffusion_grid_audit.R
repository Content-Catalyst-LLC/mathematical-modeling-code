initialize_field <- function(grid_points) {
  field <- rep(0, grid_points)
  center <- ceiling(grid_points / 2)
  field[[center]] <- 1
  field
}

diffusion_step <- function(field, stability_ratio) {
  updated <- field
  for (i in 2:(length(field) - 1)) {
    updated[[i]] <- field[[i]] + stability_ratio * (field[[i + 1]] - 2 * field[[i]] + field[[i - 1]])
  }
  updated[[1]] <- 0
  updated[[length(updated)]] <- 0
  updated
}

simulate_diffusion <- function(grid_points, diffusivity, dx, dt, steps) {
  stability_ratio <- diffusivity * dt / (dx ^ 2)
  field <- initialize_field(grid_points)
  records <- list()
  for (step in 0:steps) {
    time <- step * dt
    records[[length(records) + 1]] <- data.frame(
      step = step,
      time = time,
      center_value = field[[ceiling(grid_points / 2)]],
      total_mass = sum(field) * dx,
      max_value = max(field),
      min_value = min(field),
      stability_ratio = stability_ratio,
      warning = "Explicit diffusion schemes require stability checks; boundary and grid assumptions shape results."
    )
    field <- diffusion_step(field, stability_ratio)
  }
  do.call(rbind, records)
}

results <- simulate_diffusion(
  grid_points = 51,
  diffusivity = 0.1,
  dx = 1,
  dt = 0.25,
  steps = 100
)

summary_table <- data.frame(
  grid_points = 51,
  diffusivity = 0.1,
  dx = 1,
  dt = 0.25,
  stability_ratio = 0.1 * 0.25 / (1 ^ 2),
  interpretation = "The grid audit records how a concentrated initial field spreads under diffusion-like dynamics."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_pde_diffusion_grid_audit.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_pde_diffusion_summary.csv", row.names = FALSE)

print(head(results))
print(summary_table)
