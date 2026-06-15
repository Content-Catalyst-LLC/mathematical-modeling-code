emissions <- function(t) 50 * exp(0.015 * t)
emissions_rate <- function(t) 0.015 * emissions(t)
concentration <- function(e) 0.5 * e
d_concentration_d_emissions <- function(e) 0.5
forcing <- function(c) log(1 + c)
d_forcing_d_concentration <- function(c) 1 / (1 + c)
temperature_response <- function(f) 1.2 * f
d_temperature_d_forcing <- function(f) 1.2

chain_rule_audit <- function(t) {
  e <- emissions(t)
  c <- concentration(e)
  f <- forcing(c)
  temp <- temperature_response(f)
  s1 <- emissions_rate(t)
  s2 <- d_concentration_d_emissions(e)
  s3 <- d_forcing_d_concentration(c)
  s4 <- d_temperature_d_forcing(f)
  total <- s4 * s3 * s2 * s1
  data.frame(
    t = t,
    emissions = e,
    concentration = c,
    forcing = f,
    temperature = temp,
    emissions_rate = s1,
    d_concentration_d_emissions = s2,
    d_forcing_d_concentration = s3,
    d_temperature_d_forcing = s4,
    total_derivative = total
  )
}

results <- do.call(rbind, lapply(c(0, 5, 10, 20, 40), chain_rule_audit))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_chain_rule_pathway_audit.csv", row.names = FALSE)
print(results)
