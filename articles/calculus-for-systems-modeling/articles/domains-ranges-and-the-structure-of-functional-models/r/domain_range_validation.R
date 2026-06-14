scenarios <- read.csv("data/domain_range_scenarios.csv", stringsAsFactors = FALSE)

validate_domain <- function(initial_state, rate, capacity, time_horizon) {
  issues <- c()
  if (initial_state < 0) issues <- c(issues, "initial_state must be nonnegative")
  if (rate < 0) issues <- c(issues, "rate must be nonnegative")
  if (capacity <= 0) issues <- c(issues, "capacity must be positive")
  if (time_horizon < 0) issues <- c(issues, "time_horizon must be nonnegative")
  if (capacity > 0 && initial_state > capacity) issues <- c(issues, "initial_state exceeds capacity")
  paste(issues, collapse = "; ")
}

bounded_growth <- function(initial_state, rate, capacity, time_horizon) {
  capacity / (1 + ((capacity - initial_state) / initial_state) * exp(-rate * time_horizon))
}

rows <- list()
for (i in seq_len(nrow(scenarios))) {
  item <- scenarios[i, ]
  issues <- validate_domain(item$initial_state, item$rate, item$capacity, item$time_horizon)
  if (issues != "") {
    rows[[i]] <- data.frame(scenario = item$scenario, status = "domain_review", value = NA, issues = issues, interpretation = item$interpretation)
  } else {
    value <- bounded_growth(item$initial_state, item$rate, item$capacity, item$time_horizon)
    range_issue <- ifelse(value < 0 || value > item$capacity, "output outside expected range", "")
    rows[[i]] <- data.frame(scenario = item$scenario, status = ifelse(range_issue == "", "ok", "range_review"), value = value, issues = range_issue, interpretation = item$interpretation)
  }
}
results <- do.call(rbind, rows)
summary <- aggregate(scenario ~ status, data = results, FUN = length)
names(summary) <- c("status", "count")
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_domain_range_validation_results.csv", row.names = FALSE)
write.csv(summary, "outputs/tables/r_domain_range_validation_summary.csv", row.names = FALSE)
print(results)
print(summary)
