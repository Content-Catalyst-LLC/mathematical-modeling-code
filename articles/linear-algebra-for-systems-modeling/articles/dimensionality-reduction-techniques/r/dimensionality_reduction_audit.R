X <- matrix(
  c(
    82, 71, 18, 22, 41, 3.2,
    79, 69, 17, 20, 39, 3.0,
    85, 73, 20, 25, 43, 3.5,
    48, 52, 35, 40, 62, 6.1,
    51, 54, 38, 42, 64, 6.4,
    46, 50, 34, 39, 60, 5.9,
    68, 61, 27, 31, 52, 4.8,
    70, 63, 29, 33, 54, 5.0
  ),
  nrow = 8,
  byrow = TRUE
)

colnames(X) <- c("energy_load", "water_demand", "transport_delay", "service_backlog", "air_quality_risk", "repair_time")

reduced_dimensions <- 2
pca_model <- prcomp(X, center = TRUE, scale. = TRUE)
scores <- pca_model$x[, 1:reduced_dimensions, drop = FALSE]
loadings <- pca_model$rotation[, 1:reduced_dimensions, drop = FALSE]
scaled_X <- scale(X, center = TRUE, scale = TRUE)
reconstructed_scaled <- scores %*% t(loadings)

relative_reconstruction_error <- sqrt(sum((scaled_X - reconstructed_scaled)^2)) / sqrt(sum(scaled_X^2))
explained_variance <- pca_model$sdev^2
explained_variance_ratio <- explained_variance / sum(explained_variance)

audit_record <- data.frame(
  model_name = "synthetic_dimensionality_reduction_audit",
  observations = nrow(X),
  original_dimensions = ncol(X),
  reduced_dimensions = reduced_dimensions,
  method = "svd_based_pca_projection",
  preprocessing = "centered_and_standardized",
  preservation_target = "maximum_variance_under_linear_projection",
  explained_variance_retained = sum(explained_variance_ratio[1:reduced_dimensions]),
  relative_reconstruction_error = relative_reconstruction_error,
  validation_warning = paste(
    "Reduced representations should be validated against the task, residuals, subgroup behavior,",
    "distance distortion, reconstruction error, and sensitivity to preprocessing."
  ),
  interpretation_warning = "Dimensionality reduction preserves selected structure while discarding or distorting other structure."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_dimensionality_reduction_audit.csv", row.names = FALSE)
write.csv(scores, "outputs/tables/r_reduced_coordinates.csv")
write.csv(loadings, "outputs/tables/r_reduction_loadings.csv")
print(audit_record)
