A <- matrix(c(0.10, 1.00, 0.00, 0.20), nrow = 2, byrow = TRUE)
B <- matrix(c(0.00, 1.00), nrow = 2, byrow = TRUE)
C <- matrix(c(1.00, 0.00), nrow = 1, byrow = TRUE)
K <- matrix(c(0.50, 1.40), nrow = 1, byrow = TRUE)

A_closed <- A - B %*% K
controllability <- cbind(B, A %*% B)
observability <- rbind(C, C %*% A)

matrix_rank_2x2 <- function(M, tolerance = 1e-10) {
  if (abs(det(M)) > tolerance) return(2)
  if (any(abs(M) > tolerance)) return(1)
  return(0)
}

open_eigs <- eigen(A)$values
closed_eigs <- eigen(A_closed)$values

audit_record <- data.frame(
  system_name = "two_state_control_system_audit",
  time_model = "continuous_time_linear_state_space",
  state_matrix_A = paste(round(as.vector(t(A)), 6), collapse = ","),
  input_matrix_B = paste(round(as.vector(t(B)), 6), collapse = ","),
  output_matrix_C = paste(round(as.vector(t(C)), 6), collapse = ","),
  feedback_matrix_K = paste(round(as.vector(t(K)), 6), collapse = ","),
  open_loop_eigenvalues = paste(round(Re(open_eigs), 6), collapse = ","),
  closed_loop_eigenvalues = paste(round(Re(closed_eigs), 6), collapse = ","),
  open_loop_max_real_part = max(Re(open_eigs)),
  closed_loop_max_real_part = max(Re(closed_eigs)),
  controllability_rank = matrix_rank_2x2(controllability),
  observability_rank = matrix_rank_2x2(observability),
  interpretation_warning = paste(
    "Control models require input authority, output reliability, constraints,",
    "uncertainty review, objective transparency, and domain accountability."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_control_systems_audit.csv", row.names = FALSE)
print(audit_record)
