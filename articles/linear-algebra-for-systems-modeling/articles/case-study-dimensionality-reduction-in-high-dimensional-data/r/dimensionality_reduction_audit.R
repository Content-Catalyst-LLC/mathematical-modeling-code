features <- c("load", "temperature", "vibration", "pressure", "latency")

X <- matrix(
  c(
    80.0, 31.0, 0.42, 101.0, 14.0,
    82.0, 32.0, 0.45, 100.0, 15.0,
    78.0, 30.0, 0.41, 102.0, 13.0,
    95.0, 37.0, 0.62, 96.0, 22.0,
    97.0, 38.0, 0.65, 95.0, 24.0,
    94.0, 36.0, 0.60, 97.0, 21.0,
    70.0, 28.0, 0.35, 104.0, 11.0,
    72.0, 29.0, 0.36, 103.0, 12.0
  ),
  ncol = length(features),
  byrow = TRUE
)

colnames(X) <- features

pca <- prcomp(X, center = TRUE, scale. = TRUE)
retained <- 2

scores <- pca$x[, seq_len(retained), drop = FALSE]
loadings <- pca$rotation[, seq_len(retained), drop = FALSE]
standardized <- scale(X, center = TRUE, scale = TRUE)

reconstructed <- scores %*% t(loadings)
reconstruction_rmse <- sqrt(mean((standardized - reconstructed)^2))

explained_variance <- (pca$sdev^2) / sum(pca$sdev^2)
cumulative_explained <- sum(explained_variance[seq_len(retained)])

dominant_component_feature <- rownames(loadings)[which.max(abs(loadings[, 1]))]

audit_record <- data.frame(
  workflow_name = "dimensionality_reduction_audit",
  scenario_name = "synthetic_high_dimensional_sensor_feature_matrix",
  observation_count = nrow(X),
  feature_count = ncol(X),
  retained_components = retained,
  cumulative_explained_variance = cumulative_explained,
  reconstruction_rmse = reconstruction_rmse,
  dominant_component_feature = dominant_component_feature,
  preprocessing_summary = "Features were centered and standardized before PCA.",
  validation_warning = paste(
    "Component selection should be checked against reconstruction error, stability, subgroup error,",
    "rare-pattern preservation, and downstream task performance."
  ),
  interpretation_warning = paste(
    "Principal components are mathematical directions of variation.",
    "They are not automatically causal factors, natural categories, or decision-ready explanations."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_dimensionality_reduction_audit.csv", row.names = FALSE)
print(audit_record)
