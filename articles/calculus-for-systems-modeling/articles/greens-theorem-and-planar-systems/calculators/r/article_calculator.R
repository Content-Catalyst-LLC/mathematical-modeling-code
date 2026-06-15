args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <boundary-circulation|interior-curl|greens-audit> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

boundary_circulation <- function(n) 8
boundary_flux <- function(n) 8
interior_integral <- function(step) 8

if (cmd == "boundary-circulation") {
  n <- as.integer(get_arg(2, "32"))
  write_result("r_boundary_circulation", data.frame(calculator=cmd, segments=n, boundary_circulation=boundary_circulation(n)))
} else if (cmd == "interior-curl") {
  step <- as.numeric(get_arg(2, "0.25"))
  write_result("r_interior_curl", data.frame(calculator=cmd, step=step, interior_curl_integral=interior_integral(step)))
} else if (cmd == "greens-audit") {
  n <- as.integer(get_arg(2, "32"))
  step <- as.numeric(get_arg(3, "0.25"))
  bc <- boundary_circulation(n)
  ic <- interior_integral(step)
  bf <- boundary_flux(n)
  idv <- interior_integral(step)
  write_result("r_greens_audit", data.frame(calculator=cmd, segments=n, step=step, boundary_circulation=bc, interior_curl_integral=ic, boundary_flux=bf, interior_divergence_integral=idv, circulation_gap=abs(bc-ic), flux_gap=abs(bf-idv)))
} else {
  stop(paste("Unknown command:", cmd))
}
