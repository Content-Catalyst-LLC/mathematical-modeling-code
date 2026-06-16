args <- commandArgs(trailingOnly=TRUE)
cmd <- args[[1]]
out_dir <- "outputs"; dir.create(out_dir, recursive=TRUE, showWarnings=FALSE)
get_arg <- function(i, default) if (length(args) >= i) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names=FALSE); print(df) }
if (cmd == "left-rectangle") {
  rate_left <- as.numeric(get_arg(2, "3.2")); h <- as.numeric(get_arg(3, "0.25"))
  write_result("r_left_rectangle", data.frame(contribution=rate_left*h))
} else if (cmd == "trapezoid-step") {
  rate_left <- as.numeric(get_arg(2, "3")); rate_right <- as.numeric(get_arg(3, "4")); h <- as.numeric(get_arg(4, "0.25"))
  write_result("r_trapezoid_step", data.frame(contribution=0.5*(rate_left+rate_right)*h))
} else if (cmd == "simpson-one-third") {
  f0 <- as.numeric(get_arg(2, "2")); f1 <- as.numeric(get_arg(3, "3")); f2 <- as.numeric(get_arg(4, "2")); h <- as.numeric(get_arg(5, "0.5"))
  write_result("r_simpson_one_third", data.frame(contribution=(h/3)*(f0+4*f1+f2)))
} else if (cmd == "conservation-check") {
  initial_stock <- as.numeric(get_arg(2, "100")); final_stock <- as.numeric(get_arg(3, "130")); inflow <- as.numeric(get_arg(4, "50")); outflow <- as.numeric(get_arg(5, "20"))
  write_result("r_conservation_check", data.frame(observed_stock_change=final_stock-initial_stock, modeled_net_flow=inflow-outflow, conservation_residual=(final_stock-initial_stock)-(inflow-outflow)))
} else {
  source("../r/numerical_integration_audit.R")
}
