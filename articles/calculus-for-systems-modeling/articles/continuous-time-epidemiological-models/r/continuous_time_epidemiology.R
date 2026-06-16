basic_reproduction_number <- function(beta, gamma) {
  beta / gamma
}

simulate_sir <- function(population, susceptible0, infectious0, recovered0, beta, gamma, dt, steps) {
  s <- susceptible0
  i <- infectious0
  r <- recovered0
  peak_i <- i

  for (step in seq_len(steps)) {
    incidence <- beta * s * i / population
    recovery <- gamma * i
    s <- max(0, s - incidence * dt)
    i <- max(0, i + (incidence - recovery) * dt)
    r <- min(population, r + recovery * dt)
    peak_i <- max(peak_i, i)
  }

  c(susceptible = s, infectious = i, recovered = r, peak_infectious = peak_i)
}

simulate_seir <- function(population, susceptible0, exposed0, infectious0, recovered0, beta, sigma, gamma, dt, steps) {
  s <- susceptible0
  e <- exposed0
  i <- infectious0
  r <- recovered0
  peak_i <- i

  for (step in seq_len(steps)) {
    incidence <- beta * s * i / population
    progression <- sigma * e
    recovery <- gamma * i
    s <- max(0, s - incidence * dt)
    e <- max(0, e + (incidence - progression) * dt)
    i <- max(0, i + (progression - recovery) * dt)
    r <- min(population, r + recovery * dt)
    peak_i <- max(peak_i, i)
  }

  c(susceptible = s, exposed = e, infectious = i, recovered = r, peak_infectious = peak_i)
}

population <- 100000
dt <- 0.1
days <- 160
steps <- as.integer(days / dt)

baseline <- simulate_sir(population, 99900, 100, 0, 0.32, 0.10, dt, steps)
reduced <- simulate_sir(population, 99900, 100, 0, 0.22, 0.10, dt, steps)
seir <- simulate_seir(population, 99850, 50, 100, 0, 0.32, 0.20, 0.10, dt, steps)

scenario_records <- data.frame(
  scenario_name = c("baseline_sir", "reduced_transmission_sir", "latent_period_seir"),
  model_type = c("SIR", "SIR", "SEIR"),
  peak_infectious = c(baseline["peak_infectious"], reduced["peak_infectious"], seir["peak_infectious"]),
  final_recovered = c(baseline["recovered"], reduced["recovered"], seir["recovered"]),
  reproduction_number = c(
    basic_reproduction_number(0.32, 0.10),
    basic_reproduction_number(0.22, 0.10),
    basic_reproduction_number(0.32, 0.10)
  ),
  warning = c(
    "baseline scenario depends on homogeneous mixing assumptions",
    "reduced transmission must be tied to a mechanism",
    "exposed compartment delays infectious growth"
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(scenario_records, "outputs/tables/r_epidemiological_scenario_records.csv", row.names = FALSE)
print(scenario_records)
