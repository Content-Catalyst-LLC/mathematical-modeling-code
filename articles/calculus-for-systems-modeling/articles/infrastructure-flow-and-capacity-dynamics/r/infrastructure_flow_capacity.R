utilization <- function(arrival_rate, capacity) {
  arrival_rate / capacity
}

delay_function <- function(u, base_delay = 1, alpha = 0.8) {
  ifelse(u >= 1, Inf, base_delay * (1 + alpha * (u / (1 - u))))
}

simulate_queue <- function(arrival_rate, service_capacity, dt, steps, initial_queue = 0) {
  queue <- initial_queue
  total_utilization <- 0
  maximum_delay <- 0

  for (i in seq_len(steps)) {
    served <- min(queue + arrival_rate * dt, service_capacity * dt)
    queue <- max(0, queue + arrival_rate * dt - served)
    u <- utilization(arrival_rate, service_capacity)
    total_utilization <- total_utilization + u
    d <- delay_function(min(u, 0.999))
    maximum_delay <- max(maximum_delay, d)
  }

  c(
    final_queue = queue,
    average_utilization = total_utilization / steps,
    maximum_delay = maximum_delay
  )
}

dt <- 0.1
steps <- as.integer(24 / dt)

baseline <- simulate_queue(75, 100, dt, steps)
near_capacity <- simulate_queue(95, 100, dt, steps)
over_capacity <- simulate_queue(115, 100, dt, steps)
bottleneck <- simulate_queue(95, 90, dt, steps)

scenario_records <- data.frame(
  scenario_name = c("baseline_spare_capacity", "near_capacity_operation", "over_capacity_backlog", "series_bottleneck"),
  final_queue = c(baseline["final_queue"], near_capacity["final_queue"], over_capacity["final_queue"], bottleneck["final_queue"]),
  average_utilization = c(baseline["average_utilization"], near_capacity["average_utilization"], over_capacity["average_utilization"], bottleneck["average_utilization"]),
  maximum_delay = c(baseline["maximum_delay"], near_capacity["maximum_delay"], over_capacity["maximum_delay"], bottleneck["maximum_delay"]),
  warning = c(
    "spare capacity keeps queues low",
    "near-capacity operation creates high delay sensitivity",
    "arrival rate above capacity causes backlog accumulation",
    "minimum stage capacity limits effective throughput"
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_infrastructure_scenario_records.csv", row.names = FALSE)
print(scenario_records)
