args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <delay-steps|memory-kernel|delayed-adjustment> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "delay-steps") {
  delay <- as.numeric(get_arg(2, "5"))
  dt <- as.numeric(get_arg(3, "0.1"))
  write_result("r_delay_steps", data.frame(calculator=cmd, delay=delay, dt=dt, delay_steps=round(delay/dt)))
} else if (cmd == "memory-kernel") {
  age <- as.numeric(get_arg(2, "3"))
  decay_rate <- as.numeric(get_arg(3, "0.4"))
  write_result("r_memory_kernel", data.frame(calculator=cmd, age=age, decay_rate=decay_rate, kernel_weight=exp(-decay_rate*age)))
} else if (cmd == "delayed-adjustment") {
  initial_state <- as.numeric(get_arg(2, "80"))
  target <- as.numeric(get_arg(3, "100"))
  adjustment_rate <- as.numeric(get_arg(4, "0.2"))
  delay <- as.numeric(get_arg(5, "5"))
  dt <- as.numeric(get_arg(6, "0.1"))
  steps <- as.integer(get_arg(7, "300"))
  delay_steps <- round(delay/dt)
  states <- c(initial_state)
  rows <- list()

  for (step in 0:steps) {
    time <- step * dt
    current <- states[[length(states)]]
    delayed_index <- step - delay_steps
    delayed <- ifelse(delayed_index < 0, initial_state, states[[delayed_index + 1]])
    derivative <- adjustment_rate * (target - delayed)
    rows[[length(rows)+1]] <- data.frame(step=step, time=time, current_state=current, delayed_state=delayed, derivative_value=derivative, target=target, absolute_gap=abs(current-target))
    states <- c(states, current + dt * derivative)
  }

  write_result("r_delayed_adjustment", do.call(rbind, rows))
} else {
  stop(paste("Unknown command:", cmd))
}
