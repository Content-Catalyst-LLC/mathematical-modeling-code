args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <diffusion-ratio|transport-ratio|advection-diffusion-step|advection-diffusion-simulation> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "diffusion-ratio") {
  diffusivity <- as.numeric(get_arg(2, "0.08"))
  dt <- as.numeric(get_arg(3, "0.2"))
  dx <- as.numeric(get_arg(4, "1"))
  write_result("r_diffusion_ratio", data.frame(calculator=cmd, diffusivity=diffusivity, dt=dt, dx=dx, diffusion_ratio=diffusivity*dt/(dx^2)))
} else if (cmd == "transport-ratio") {
  velocity <- as.numeric(get_arg(2, "0.4"))
  dt <- as.numeric(get_arg(3, "0.2"))
  dx <- as.numeric(get_arg(4, "1"))
  write_result("r_transport_ratio", data.frame(calculator=cmd, velocity=velocity, dt=dt, dx=dx, transport_ratio=velocity*dt/dx))
} else if (cmd == "advection-diffusion-step") {
  left <- as.numeric(get_arg(2, "0"))
  center <- as.numeric(get_arg(3, "1"))
  right <- as.numeric(get_arg(4, "0"))
  d_ratio <- as.numeric(get_arg(5, "0.016"))
  t_ratio <- as.numeric(get_arg(6, "0.08"))
  updated <- center + d_ratio * (right - 2 * center + left) - t_ratio * (center - left)
  write_result("r_advection_diffusion_step", data.frame(calculator=cmd, left=left, center=center, right=right, diffusion_ratio=d_ratio, transport_ratio=t_ratio, updated_center=updated))
} else if (cmd == "advection-diffusion-simulation") {
  grid_points <- as.integer(get_arg(2, "61"))
  diffusivity <- as.numeric(get_arg(3, "0.08"))
  velocity <- as.numeric(get_arg(4, "0.4"))
  dx <- as.numeric(get_arg(5, "1"))
  dt <- as.numeric(get_arg(6, "0.2"))
  steps <- as.integer(get_arg(7, "120"))
  d_ratio <- diffusivity * dt / (dx ^ 2)
  t_ratio <- velocity * dt / dx
  field <- rep(0, grid_points)
  field[[ceiling(grid_points / 2)]] <- 1
  rows <- list()
  for (step in 0:steps) {
    rows[[length(rows)+1]] <- data.frame(step=step, time=step*dt, center_value=field[[ceiling(grid_points/2)]], total_mass=sum(field)*dx, max_value=max(field), min_value=min(field), diffusion_ratio=d_ratio, transport_ratio=t_ratio)
    updated <- field
    for (i in 2:(grid_points-1)) {
      updated[[i]] <- field[[i]] + d_ratio * (field[[i+1]] - 2 * field[[i]] + field[[i-1]]) - t_ratio * (field[[i]] - field[[i-1]])
    }
    updated[[1]] <- 0
    updated[[grid_points]] <- 0
    field <- updated
  }
  write_result("r_advection_diffusion_simulation", do.call(rbind, rows))
} else {
  stop(paste("Unknown command:", cmd))
}
