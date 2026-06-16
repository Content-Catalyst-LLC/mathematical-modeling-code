args <- commandArgs(trailingOnly=TRUE)
cmd <- args[[1]]
out_dir <- "outputs"; dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)
get_arg <- function(i, default) if (length(args) >= i) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names=FALSE); print(df) }
if (cmd == "diffusion-ratio") {
  d <- as.numeric(get_arg(2, "0.08")); dt <- as.numeric(get_arg(3, "0.2")); dx <- as.numeric(get_arg(4, "1"))
  write_result("r_diffusion_ratio", data.frame(diffusion_ratio=d*dt/(dx^2)))
} else if (cmd == "central-difference") {
  fp <- as.numeric(get_arg(2, "1")); fn <- as.numeric(get_arg(3, "1.2")); dx <- as.numeric(get_arg(4, "0.1"))
  write_result("r_central_difference", data.frame(derivative_estimate=(fn-fp)/(2*dx)))
} else if (cmd == "second-central-difference") {
  fp <- as.numeric(get_arg(2, "1")); fc <- as.numeric(get_arg(3, "1.2")); fn <- as.numeric(get_arg(4, "1.4")); dx <- as.numeric(get_arg(5, "0.1"))
  write_result("r_second_central_difference", data.frame(second_derivative_estimate=(fn-2*fc+fp)/(dx^2)))
} else if (cmd == "explicit-diffusion-step") {
  left <- as.numeric(get_arg(2, "0")); center <- as.numeric(get_arg(3, "1")); right <- as.numeric(get_arg(4, "0")); ratio <- as.numeric(get_arg(5, "0.016"))
  write_result("r_explicit_diffusion_step", data.frame(updated_center=center+ratio*(right-2*center+left)))
} else if (cmd == "stability-check") {
  d <- as.numeric(get_arg(2, "0.08")); dt <- as.numeric(get_arg(3, "0.2")); dx <- as.numeric(get_arg(4, "1"))
  ratio <- d*dt/(dx^2); status <- ifelse(ratio <= 0.5, "stable_for_basic_explicit_1d_diffusion", "unstable_risk")
  write_result("r_stability_check", data.frame(diffusion_ratio=ratio, stability_status=status))
} else {
  stop("Unknown command")
}
