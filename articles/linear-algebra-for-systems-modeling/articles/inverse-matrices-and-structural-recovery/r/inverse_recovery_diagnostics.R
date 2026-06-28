# Inverse Matrices and Structural Recovery
# Engineer-grade diagnostics in base R.

recovery_report <- function(A, b, label) {
  cat("\n===", label, "===\n")
  cat("A:\n")
  print(A)
  cat("b:\n")
  print(b)

  rank_A <- qr(A)$rank
  det_A <- if (nrow(A) == ncol(A)) det(A) else NA
  cond_A <- kappa(A)

  cat("rank(A):", rank_A, "\n")
  cat("det(A):", det_A, "\n")
  cat("condition number estimate:", cond_A, "\n")

  if (nrow(A) == ncol(A) && rank_A == ncol(A)) {
    x_hat <- solve(A, b)
    residual <- A %*% x_hat - b

    cat("method: solve(A, b)\n")
    cat("x_hat:\n")
    print(x_hat)
    cat("residual norm:", sqrt(sum(residual^2)), "\n")
  } else {
    cat("Matrix is not square/full-rank. Use least squares or pseudoinverse methods.\n")
  }
}

A <- matrix(c(3, 2, 1, 4), nrow = 2)
x_true <- matrix(c(2, 1), nrow = 2)
b <- A %*% x_true
recovery_report(A, b, "well-conditioned square recovery")

A_bad <- matrix(c(1, 1, 1, 1.0001), nrow = 2)
b_bad <- A_bad %*% matrix(c(1, 1), nrow = 2)
recovery_report(A_bad, b_bad, "near-singular recovery")
