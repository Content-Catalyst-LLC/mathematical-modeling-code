# Linear Algebra for Systems Modeling:
# Matrix analysis, eigenstructure, and PCA in R.
# Educational example only.

library(tidyverse)

systems_data <- read_csv("../data/systems_observations.csv", show_col_types = FALSE)

X <- systems_data |>
  select(-observation_id) |>
  scale()

correlation_matrix <- cor(X)

eigen_results <- eigen(correlation_matrix)

eigen_summary <- tibble(
  component = paste0("component_", seq_along(eigen_results$values)),
  eigenvalue = eigen_results$values,
  variance_share = eigen_results$values / sum(eigen_results$values)
)

pca_model <- prcomp(X, center = FALSE, scale. = FALSE)

pca_scores <- as_tibble(pca_model$x) |>
  mutate(observation_id = systems_data$observation_id)

pca_loadings <- as_tibble(pca_model$rotation, rownames = "variable")

pca_variance <- tibble(
  component = paste0("PC", seq_along(pca_model$sdev)),
  standard_deviation = pca_model$sdev,
  variance = pca_model$sdev^2,
  variance_share = (pca_model$sdev^2) / sum(pca_model$sdev^2)
)

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(as_tibble(correlation_matrix, rownames = "variable"), "../outputs/r_correlation_matrix.csv")
write_csv(eigen_summary, "../outputs/r_eigen_summary.csv")
write_csv(pca_scores, "../outputs/r_pca_scores.csv")
write_csv(pca_loadings, "../outputs/r_pca_loadings.csv")
write_csv(pca_variance, "../outputs/r_pca_variance.csv")

print(eigen_summary)
print(pca_variance)
