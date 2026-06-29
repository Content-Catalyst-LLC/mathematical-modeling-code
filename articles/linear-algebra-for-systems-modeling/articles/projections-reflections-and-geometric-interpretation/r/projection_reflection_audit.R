x <- c(4, 3)
direction <- c(2, 1)
u <- direction / sqrt(sum(direction^2))

P <- u %*% t(u)
projected <- as.vector(P %*% x)
residual <- x - projected
residual_norm <- sqrt(sum(residual^2))

I <- diag(2)
R <- 2 * P - I
reflected <- as.vector(R %*% x)

audit_record <- data.frame(
  system_name = "two_dimensional_geometric_transformation_audit",
  original_vector = paste(round(x, 6), collapse = ","),
  unit_direction = paste(round(u, 6), collapse = ","),
  projected_vector = paste(round(projected, 6), collapse = ","),
  residual_vector = paste(round(residual, 6), collapse = ","),
  residual_norm = residual_norm,
  reflected_vector = paste(round(reflected, 6), collapse = ","),
  projection_idempotence_error = sqrt(sum((P %*% P - P)^2)),
  projection_symmetry_error = sqrt(sum((t(P) - P)^2)),
  reflection_involution_error = sqrt(sum((R %*% R - I)^2)),
  length_preservation_error = abs(sqrt(sum(reflected^2)) - sqrt(sum(x^2))),
  interpretation_warning = "Projection and reflection interpretation depends on geometry, units, scaling, and model purpose."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_projection_reflection_audit.csv", row.names = FALSE)
print(audit_record)
