variable_names <- c("energy_load", "water_demand", "transport_delay", "service_backlog", "air_quality_risk")

X <- matrix(
  c(
    82, 71, 18, 22, 41,
    79, 69, 17, 20, 39,
    85, 73, 20, 25, 43,
    48, 52, 35, 40, 62,
    51, 54, 38, 42, 64,
    46, 50, 34, 39, 60,
    68, 61, 27, 31, 52,
    70, 63, 29, 33, 54
  ),
  nrow = 8,
  byrow = TRUE
)

colnames(X) <- variable_names
retained_components <- 2
pca_model <- prcomp(X, center = TRUE, scale. = TRUE)

explained_variance <- pca_model$sdev^2
explained_variance_ratio <- explained_variance / sum(explained_variance)

scores <- pca_model$x[, 1:retained_components, drop = FALSE]
loadings <- pca_model$rotation[, 1:retained_components, drop = FALSE]

reconstructed_scaled <- scores %*% t(loadings)
scaled_X <- scale(X, center = TRUE, scale = TRUE)
relative_reconstruction_error <- sqrt(sum((scaled_X - reconstructed_scaled)^2)) / sqrt(sum(scaled_X^2))

audit_record <- data.frame(
  model_name = "synthetic_pca_diagnostic_audit",
  observations = nrow(X),
  variables = ncol(X),
  preprocessing = "centered_and_standardized",
  retained_components = retained_components,
  explained_variance_ratio = paste(signif(explained_variance_ratio, 12), collapse = ";"),
  cumulative_explained_variance = sum(explained_variance_ratio[1:retained_components]),
  relative_reconstruction_error = relative_reconstruction_error,
  largest_loading_variable_pc1 = rownames(loadings)[which.max(abs(loadings[, 1]))],
  largest_loading_variable_pc2 = rownames(loadings)[which.max(abs(loadings[, 2]))],
  interpretation_warning = paste(
    "PCA components depend on data matrix construction, centering, scaling, outliers,",
    "retained-rank choice, explained-variance criteria, residual review, and domain interpretation."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_pca_diagnostic_audit.csv", row.names = FALSE)
write.csv(scores, "outputs/tables/r_pca_scores.csv")
write.csv(loadings, "outputs/tables/r_pca_loadings.csv")
print(audit_record)
