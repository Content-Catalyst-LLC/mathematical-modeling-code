a <- c(3, 1, 2)
b <- c(1, -1, -1)

dot_ab <- sum(a * b)
tol <- 1e-10
orthogonal_under_tolerance <- abs(dot_ab) <= tol

norm2 <- function(x) sqrt(sum(x^2))
unit_a <- a / norm2(a)
unit_b <- b / norm2(b)

projection_of_a_onto_b <- (sum(a * b) / sum(b * b)) * b
residual <- a - projection_of_a_onto_b
residual_norm <- norm2(residual)

Q <- cbind(unit_a, unit_b)
orthonormality_error <- sqrt(sum((t(Q) %*% Q - diag(2))^2))

audit_record <- data.frame(
  system_name = "three_component_orthogonality_audit",
  vector_a = paste(round(a, 6), collapse = ","),
  vector_b = paste(round(b, 6), collapse = ","),
  dot_product = dot_ab,
  orthogonal_under_tolerance = orthogonal_under_tolerance,
  unit_a = paste(round(unit_a, 6), collapse = ","),
  unit_b = paste(round(unit_b, 6), collapse = ","),
  projection_of_a_onto_b = paste(round(projection_of_a_onto_b, 6), collapse = ","),
  residual_vector = paste(round(residual, 6), collapse = ","),
  residual_norm = residual_norm,
  orthonormality_error = orthonormality_error,
  interpretation_warning = paste(
    "Orthogonality depends on the chosen inner product, scaling, units, and tolerance.",
    "Orthogonal residuals may still contain important excluded structure."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_orthogonality_audit.csv", row.names = FALSE)
print(audit_record)
