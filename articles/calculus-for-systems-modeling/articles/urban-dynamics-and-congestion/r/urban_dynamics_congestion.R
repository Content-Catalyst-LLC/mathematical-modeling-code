traffic_flow <- function(density, free_flow_speed, jam_density) {
  max(0, free_flow_speed * density * (1 - density / jam_density))
}

queue_step <- function(queue, arrival_rate, service_rate, dt) {
  max(0, queue + (arrival_rate - service_rate) * dt)
}

simulate_queue <- function(arrival_rate, service_rate, duration, dt) {
  queue <- 0
  total_delay <- 0
  steps <- as.integer(duration / dt)
  for (step in seq_len(steps)) {
    queue <- queue_step(queue, arrival_rate, service_rate, dt)
    total_delay <- total_delay + queue * dt
  }
  c(final_queue = queue, total_delay = total_delay)
}

bpr_travel_time <- function(free_flow_time, volume, capacity, alpha = 0.15, beta = 4) {
  free_flow_time * (1 + alpha * (volume / capacity)^beta)
}

induced_demand_step <- function(volume, target_volume, adjustment_rate, dt) {
  volume + adjustment_rate * (target_volume - volume) * dt
}

duration <- 3
dt <- 0.01
free_flow_time <- 20

below <- simulate_queue(1800, 2000, duration, dt)
over <- simulate_queue(2300, 2000, duration, dt)
expanded <- simulate_queue(2300, 2600, duration, dt)
transit_priority <- simulate_queue(1200, 1600, duration, dt)

induced_volume <- 2300
for (i in seq_len(10)) {
  induced_volume <- induced_demand_step(induced_volume, 2600, 0.15, 1)
}

scenario_records <- data.frame(
  scenario_name = c("below_capacity_corridor","over_capacity_bottleneck","capacity_expansion_with_induced_demand","transit_priority_case"),
  model_type = c("queue_and_bpr","queue_and_bpr","capacity_adjustment","multimodal_capacity"),
  demand = c(1800, 2300, induced_volume, 1200),
  capacity = c(2000, 2000, 2600, 1600),
  final_queue = c(below["final_queue"], over["final_queue"], expanded["final_queue"], transit_priority["final_queue"]),
  total_delay = c(below["total_delay"], over["total_delay"], expanded["total_delay"], transit_priority["total_delay"]),
  travel_time = c(
    bpr_travel_time(free_flow_time, 1800, 2000),
    bpr_travel_time(free_flow_time, 2300, 2000),
    bpr_travel_time(free_flow_time, induced_volume, 2600),
    bpr_travel_time(free_flow_time, 1200, 1600)
  ),
  warning = c(
    "demand below capacity produces limited queue accumulation",
    "demand above capacity produces persistent queue and delay",
    "capacity expansion may reduce delay while long-run demand adjusts upward",
    "transit priority should be evaluated through person throughput"
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_urban_congestion_scenario_records.csv", row.names = FALSE)
print(scenario_records)
