args <- commandArgs(trailingOnly = TRUE)
cmd <- ifelse(length(args) >= 1, args[[1]], "logistic")
out_dir <- "outputs"; dir.create(out_dir, recursive = TRUE, showWarnings = FALSE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
if (cmd == "logistic") {
  n0 <- as.numeric(get_arg(2, "100")); r <- as.numeric(get_arg(3, "0.08")); k <- as.numeric(get_arg(4, "1000")); t <- as.numeric(get_arg(5, "40"))
  pop <- k/(1+((k-n0)/n0)*exp(-r*t))
  out <- data.frame(calculator=cmd,n0=n0,r=r,k=k,t=t,population=pop,capacity_fraction=pop/k,warning="Carrying capacity is assumption-bearing.")
} else {
  n0 <- as.numeric(get_arg(2, "100")); r <- as.numeric(get_arg(3, "0.08")); t <- as.numeric(get_arg(4, "40"))
  pop <- n0*exp(r*t)
  out <- data.frame(calculator=cmd,n0=n0,r=r,t=t,population=pop,warning="Exponential growth is an unconstrained baseline.")
}
write.csv(out, file.path(out_dir, paste0("r_", cmd, ".csv")), row.names=FALSE)
print(out)
