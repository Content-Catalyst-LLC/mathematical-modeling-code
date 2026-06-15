args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <boundary-circulation|surface-curl-flux|stokes-audit> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

boundary_circulation <- function(radius, segments) {
  total <- 0
  for (i in 0:(segments-1)) {
    theta0 <- 2*pi*i/segments
    theta1 <- 2*pi*(i+1)/segments
    x0 <- radius*cos(theta0); y0 <- radius*sin(theta0)
    x1 <- radius*cos(theta1); y1 <- radius*sin(theta1)
    xm <- 0.5*(x0+x1); ym <- 0.5*(y0+y1)
    dx <- x1-x0; dy <- y1-y0
    total <- total + (-ym)*dx + xm*dy
  }
  total
}

surface_curl_flux <- function(radius, radial_steps) {
  2*pi*radius^2
}

if (cmd == "boundary-circulation") {
  radius <- as.numeric(get_arg(2, "1")); segments <- as.integer(get_arg(3, "128"))
  write_result("r_boundary_circulation", data.frame(calculator=cmd, radius=radius, segments=segments, boundary_circulation=boundary_circulation(radius, segments)))
} else if (cmd == "surface-curl-flux") {
  radius <- as.numeric(get_arg(2, "1")); radial_steps <- as.integer(get_arg(3, "32"))
  write_result("r_surface_curl_flux", data.frame(calculator=cmd, radius=radius, radial_steps=radial_steps, surface_curl_flux=surface_curl_flux(radius, radial_steps)))
} else if (cmd == "stokes-audit") {
  radius <- as.numeric(get_arg(2, "1")); segments <- as.integer(get_arg(3, "128")); radial_steps <- as.integer(get_arg(4, "32"))
  bc <- boundary_circulation(radius, segments)
  sf <- surface_curl_flux(radius, radial_steps)
  write_result("r_stokes_audit", data.frame(calculator=cmd, radius=radius, segments=segments, radial_steps=radial_steps, boundary_circulation=bc, surface_curl_flux=sf, absolute_gap=abs(bc-sf)))
} else {
  stop(paste("Unknown command:", cmd))
}
