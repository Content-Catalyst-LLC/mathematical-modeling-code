args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <damping-classification|period|acceleration> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

classify <- function(zeta) {
  if (zeta == 0) return("undamped")
  if (zeta > 0 && zeta < 1) return("underdamped")
  if (zeta == 1) return("critically_damped")
  "overdamped"
}

forcing <- function(t, amplitude, frequency) amplitude * cos(frequency * t)

accel <- function(x, v, t, zeta, omega, amp, freq) {
  forcing(t, amp, freq) - 2*zeta*omega*v - omega^2*x
}

if (cmd == "damping-classification") {
  zeta <- as.numeric(get_arg(2, "0.2"))
  write_result("r_damping_classification", data.frame(calculator=cmd, damping_ratio=zeta, classification=classify(zeta)))
} else if (cmd == "period") {
  omega <- as.numeric(get_arg(2, "1"))
  write_result("r_period", data.frame(calculator=cmd, natural_frequency=omega, period=2*pi/omega))
} else if (cmd == "acceleration") {
  x <- as.numeric(get_arg(2, "1")); v <- as.numeric(get_arg(3, "0")); t <- as.numeric(get_arg(4, "0"))
  zeta <- as.numeric(get_arg(5, "0.2")); omega <- as.numeric(get_arg(6, "1")); amp <- as.numeric(get_arg(7, "0")); freq <- as.numeric(get_arg(8, "1"))
  write_result("r_acceleration", data.frame(calculator=cmd, position=x, velocity=v, time=t, damping_ratio=zeta, natural_frequency=omega, forcing_amplitude=amp, forcing_frequency=freq, acceleration=accel(x,v,t,zeta,omega,amp,freq)))
} else {
  stop(paste("Unknown command:", cmd))
}
