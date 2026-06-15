args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <vector-field|circle-circulation|circle-flux> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

vector_field <- function(x, y) c(-y, x)
dot_product <- function(a, b) sum(a*b)

circle_summary <- function(radius, segments) {
  flux <- 0
  circulation <- 0
  for (i in 0:(segments-1)) {
    theta0 <- 2*pi*i/segments
    theta1 <- 2*pi*(i+1)/segments
    x0 <- radius*cos(theta0); y0 <- radius*sin(theta0)
    x1 <- radius*cos(theta1); y1 <- radius*sin(theta1)
    xm <- 0.5*(x0+x1); ym <- 0.5*(y0+y1)
    dx <- x1-x0; dy <- y1-y0
    segment_length <- sqrt(dx^2 + dy^2)
    normal <- c(xm/radius, ym/radius)
    field <- vector_field(xm, ym)
    flux <- flux + dot_product(field, normal) * segment_length
    circulation <- circulation + dot_product(field, c(dx, dy))
  }
  c(flux=flux, circulation=circulation)
}

if (cmd == "vector-field") {
  x <- as.numeric(get_arg(2, "1")); y <- as.numeric(get_arg(3, "0"))
  v <- vector_field(x,y)
  write_result("r_vector_field", data.frame(calculator=cmd, x=x, y=y, fx=v[1], fy=v[2]))
} else if (cmd == "circle-circulation") {
  radius <- as.numeric(get_arg(2, "1")); segments <- as.integer(get_arg(3, "64"))
  s <- circle_summary(radius, segments)
  write_result("r_circle_circulation", data.frame(calculator=cmd, radius=radius, segments=segments, circulation=s["circulation"]))
} else if (cmd == "circle-flux") {
  radius <- as.numeric(get_arg(2, "1")); segments <- as.integer(get_arg(3, "64"))
  s <- circle_summary(radius, segments)
  write_result("r_circle_flux", data.frame(calculator=cmd, radius=radius, segments=segments, flux=s["flux"]))
} else {
  stop(paste("Unknown command:", cmd))
}
