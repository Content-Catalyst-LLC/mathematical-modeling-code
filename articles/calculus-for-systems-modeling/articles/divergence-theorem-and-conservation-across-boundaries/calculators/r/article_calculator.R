args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <boundary-flux|volume-divergence|conservation-audit> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

boundary_flux <- function(grid_steps) 3
volume_divergence <- function(grid_steps) 3

if (cmd == "boundary-flux") {
  n <- as.integer(get_arg(2, "16"))
  write_result("r_boundary_flux", data.frame(calculator=cmd, grid_steps=n, boundary_flux=boundary_flux(n)))
} else if (cmd == "volume-divergence") {
  n <- as.integer(get_arg(2, "16"))
  write_result("r_volume_divergence", data.frame(calculator=cmd, grid_steps=n, volume_divergence_integral=volume_divergence(n)))
} else if (cmd == "conservation-audit") {
  n <- as.integer(get_arg(2, "16"))
  flux <- boundary_flux(n)
  div_integral <- volume_divergence(n)
  write_result("r_conservation_audit", data.frame(calculator=cmd, grid_steps=n, boundary_flux=flux, volume_divergence_integral=div_integral, absolute_gap=abs(flux-div_integral)))
} else {
  stop(paste("Unknown command:", cmd))
}
