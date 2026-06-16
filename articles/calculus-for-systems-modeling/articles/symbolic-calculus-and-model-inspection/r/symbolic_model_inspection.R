output_dir <- "outputs"
dir.create(file.path(output_dir, "tables"), recursive = TRUE, showWarnings = FALSE)
dir.create(file.path(output_dir, "reports"), recursive = TRUE, showWarnings = FALSE)

rate_expression <- expression(r * x * (1 - x / K))
first_derivative <- D(rate_expression[[1]], "x")
second_derivative <- D(first_derivative, "x")

records <- data.frame(
  item = c("rate_expression", "first_derivative", "second_derivative", "equilibrium_condition", "domain_warning"),
  expression = c(
    deparse(rate_expression[[1]]),
    deparse(first_derivative),
    deparse(second_derivative),
    "r * x * (1 - x / K) = 0",
    "x, r, and K should be interpreted under documented domain assumptions"
  ),
  interpretation = c(
    "Logistic growth rate expression.",
    "Marginal growth effect with respect to x.",
    "Curvature of the rate expression.",
    "Equilibria occur where the rate expression equals zero.",
    "Symbolic interpretation depends on assumptions and valid domains."
  ),
  warning = c(
    "K must be nonzero.",
    "Derivative interpretation depends on domain.",
    "Curvature does not validate empirical structure.",
    "Solving requires domain review.",
    "Automatic simplification can hide excluded cases."
  )
)

write.csv(records, file.path(output_dir, "tables", "r_symbolic_expression_records.csv"), row.names = FALSE)

report <- c(
  "# R Symbolic Expression Records",
  "",
  paste("Rate expression:", deparse(rate_expression[[1]])),
  paste("First derivative:", deparse(first_derivative)),
  paste("Second derivative:", deparse(second_derivative)),
  "",
  "Symbolic records should preserve assumptions, domains, and warnings."
)

writeLines(report, file.path(output_dir, "reports", "r_symbolic_expression_records.md"))
print(records)
