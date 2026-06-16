args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <rk4-step|midpoint-step|heun-step|stage-values> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

rate <- function(t, y, decay_rate) -decay_rate * y
stage_values <- function(t, y, h, decay_rate) {
  k1 <- rate(t, y, decay_rate)
  k2 <- rate(t + h / 2, y + h * k1 / 2, decay_rate)
  k3 <- rate(t + h / 2, y + h * k2 / 2, decay_rate)
  k4 <- rate(t + h, y + h * k3, decay_rate)
  data.frame(k1=k1, k2=k2, k3=k3, k4=k4)
}

t <- as.numeric(get_arg(2, "0"))
y <- as.numeric(get_arg(3, "100"))
h <- as.numeric(get_arg(4, "0.5"))
decay_rate <- as.numeric(get_arg(5, "0.35"))

if (cmd == "rk4-step") {
  s <- stage_values(t, y, h, decay_rate)
  updated <- y + (h / 6) * (s$k1 + 2*s$k2 + 2*s$k3 + s$k4)
  write_result("r_rk4_step", data.frame(calculator=cmd, t=t, y=y, h=h, decay_rate=decay_rate, updated_value=updated))
} else if (cmd == "midpoint-step") {
  k1 <- rate(t, y, decay_rate)
  k2 <- rate(t + h / 2, y + h * k1 / 2, decay_rate)
  write_result("r_midpoint_step", data.frame(calculator=cmd, t=t, y=y, h=h, decay_rate=decay_rate, updated_value=y + h*k2))
} else if (cmd == "heun-step") {
  k1 <- rate(t, y, decay_rate)
  k2 <- rate(t + h, y + h * k1, decay_rate)
  write_result("r_heun_step", data.frame(calculator=cmd, t=t, y=y, h=h, decay_rate=decay_rate, updated_value=y + h*0.5*(k1+k2)))
} else if (cmd == "stage-values") {
  s <- stage_values(t, y, h, decay_rate)
  write_result("r_stage_values", cbind(data.frame(calculator=cmd, t=t, y=y, h=h, decay_rate=decay_rate), s))
} else {
  stop(paste("Unknown command:", cmd))
}
