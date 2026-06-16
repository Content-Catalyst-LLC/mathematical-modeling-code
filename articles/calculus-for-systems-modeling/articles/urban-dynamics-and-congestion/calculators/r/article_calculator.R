args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <traffic-flow|bpr-travel-time> ...")
cmd <- args[[1]]
out_dir <- "outputs"
dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default

if (cmd == "traffic-flow") {
  density <- as.numeric(get_arg(2, "35"))
  free_flow_speed <- as.numeric(get_arg(3, "60"))
  jam_density <- as.numeric(get_arg(4, "140"))
  value <- max(0, free_flow_speed * density * (1 - density / jam_density))
  out <- data.frame(calculator = cmd, density = density, free_flow_speed = free_flow_speed, jam_density = jam_density, flow = value, warning = "Fundamental diagrams are context-specific not universal laws.")
} else if (cmd == "bpr-travel-time") {
  free_flow_time <- as.numeric(get_arg(2, "20"))
  volume <- as.numeric(get_arg(3, "2300"))
  capacity <- as.numeric(get_arg(4, "2000"))
  value <- free_flow_time * (1 + 0.15 * (volume / capacity)^4)
  out <- data.frame(calculator = cmd, free_flow_time = free_flow_time, volume = volume, capacity = capacity, travel_time = value, delay = value - free_flow_time, warning = "Travel-time functions should be calibrated and not treated as universal.")
} else {
  stop(paste("Unknown command:", cmd))
}

write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names = FALSE)
print(out)
