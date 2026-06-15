resource_stock <- function(t) 1000 * exp(-0.01 * t)
resource_stock_rate <- function(t) -0.01 * resource_stock(t)
population <- function(t) 100 * exp(0.02 * t)
population_rate <- function(t) 0.02 * population(t)

quotient_audit <- function(t) {
  f <- resource_stock(t)
  g <- population(t)
  fp <- resource_stock_rate(t)
  gp <- population_rate(t)
  if (abs(g) < 1e-8) stop("denominator too close to zero")
  ratio <- f / g
  numerator_effect <- fp / g
  denominator_effect <- -(f * gp) / (g^2)
  quotient_derivative <- numerator_effect + denominator_effect
  data.frame(
    t = t,
    numerator = f,
    denominator = g,
    ratio = ratio,
    numerator_rate = fp,
    denominator_rate = gp,
    numerator_effect = numerator_effect,
    denominator_effect = denominator_effect,
    quotient_derivative = quotient_derivative,
    numerator_relative_rate = fp / f,
    denominator_relative_rate = gp / g,
    ratio_relative_rate = quotient_derivative / ratio
  )
}

results <- do.call(rbind, lapply(c(0, 5, 10, 20, 40), quotient_audit))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_quotient_rule_relative_change.csv", row.names = FALSE)
print(results)
