population <- function(t) 100 * exp(0.01 * t)
population_rate <- function(t) 0.01 * population(t)
affluence <- function(t) 2 * exp(0.02 * t)
affluence_rate <- function(t) 0.02 * affluence(t)

product_rule_audit <- function(t) {
  a <- population_rate(t) * affluence(t)
  b <- population(t) * affluence_rate(t)
  total <- a + b
  data.frame(rule="product_rule", model_structure="impact = population * affluence", t=t, derivative_total=total, population_component=a, affluence_component=b, population_share=a/total, affluence_share=b/total)
}

results <- do.call(rbind, lapply(c(0, 5, 10, 20), product_rule_audit))
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_product_rule_sensitivity_decomposition.csv", row.names = FALSE)
print(results)
