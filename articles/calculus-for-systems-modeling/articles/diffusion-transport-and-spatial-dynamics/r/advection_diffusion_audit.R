initialize_field <- function(grid_points) {
  field <- rep(0, grid_points)
  center <- ceiling(grid_points / 2)
  field[[center]] <- 1
  field
}

update_advection_diffusion <- function(field, diffusion_ratio, transport_ratio) {
  updated <- field
  for (i in 2:(length(field) - 1)) {
    diffusion_part <- diffusion_ratio * (field[[i + 1]] - 2 * field[[i]] + field[[i - 1]])
    transport_part <- -transport_ratio * (field[[i]] - field[[i - 1]])
    updated[[i]] <- field[[i]] + diffusion_part + transport_part
  }
  updated[[1]] <- 0
  updated[[length(updated)]] <- 0
  updated
}

simulate_spatial_dynamics <- function(grid_points, diffusivity, velocity, dx, dt, steps) {
  diffusion_ratio <- diffusivity * dt / (dx ^ 2)
  transport_ratio <- velocity * dt / dx
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
      diffusion_ratio = diffusion_ratio,
      transport_ratio = transport_ratio,
      warning = "Spatial dynamics depend on field meaning, boundary conditions, grid spacing, time step, and numerical stability."
    )
    field <- update_advection_diffusion(field, diffusion_ratio, transport_ratio)
  }
  do.call(rbind, records)
}

results <- simulate_spatial_dynamics(
  grid_points = 61,
  diffusivity = 0.08,
  velocity = 0.4,
  dx = 1,
  dt = 0.2,
  steps = 120
)

summary_table <- data.frame(
  grid_points = 61,
  diffusivity = 0.08,
  velocity = 0.4,
  dx = 1,
  dt = 0.2,
  diffusion_ratio = 0.08 * 0.2 / (1 ^ 2),
  transport_ratio = 0.4 * 0.2 / 1,
  interpretation = "The audit records how a localized field moves and spreads under transport and diffusion."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_advection_diffusion_audit.csv", row.names = FALSE)
write.csv(summary_table, "outputs/tables/r_advection_diffusion_summary.csv", row.names = FALSE)

print(head(results))
print(summary_table)
