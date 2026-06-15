args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <stability-ratio|diffusion-step|explicit-diffusion> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "stability-ratio") {
  diffusivity <- as.numeric(get_arg(2, "0.1"))
  dt <- as.numeric(get_arg(3, "0.25"))
  dx <- as.numeric(get_arg(4, "1"))
  r <- diffusivity * dt / (dx ^ 2)
  write_result("r_stability_ratio", data.frame(calculator=cmd, diffusivity=diffusivity, dt=dt, dx=dx, stability_ratio=r, usually_stable_for_1d_explicit_diffusion=r <= 0.5))
} else if (cmd == "diffusion-step") {
  left <- as.numeric(get_arg(2, "0"))
  center <- as.numeric(get_arg(3, "1"))
  right <- as.numeric(get_arg(4, "0"))
  ratio <- as.numeric(get_arg(5, "0.025"))
  updated <- center + ratio * (right - 2 * center + left)
  write_result("r_diffusion_step", data.frame(calculator=cmd, left=left, center=center, right=right, stability_ratio=ratio, updated_center=updated))
} else if (cmd == "explicit-diffusion") {
  grid_points <- as.integer(get_arg(2, "51"))
  diffusivity <- as.numeric(get_arg(3, "0.1"))
  dx <- as.numeric(get_arg(4, "1"))
  dt <- as.numeric(get_arg(5, "0.25"))
  steps <- as.integer(get_arg(6, "100"))
  ratio <- diffusivity * dt / (dx ^ 2)
  field <- rep(0, grid_points)
  field[[ceiling(grid_points / 2)]] <- 1
  rows <- list()
  for (step in 0:steps) {
    rows[[length(rows)+1]] <- data.frame(step=step, time=step*dt, center_value=field[[ceiling(grid_points/2)]], total_mass=sum(field)*dx, max_value=max(field), min_value=min(field), stability_ratio=ratio)
    updated <- field
    for (i in 2:(grid_points-1)) {
      updated[[i]] <- field[[i]] + ratio * (field[[i+1]] - 2 * field[[i]] + field[[i-1]])
    }
    updated[[1]] <- 0
    updated[[grid_points]] <- 0
    field <- updated
  }
  write_result("r_explicit_diffusion", do.call(rbind, rows))
} else {
  stop(paste("Unknown command:", cmd))
}
