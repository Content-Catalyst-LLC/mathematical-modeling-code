state_a <- c(12.0, 4.0, 0.8)
state_b <- c(10.0, 5.5, 1.1)

difference <- state_a - state_b
dot_product <- sum(state_a * state_b)

norm1 <- function(x) sum(abs(x))
norm2 <- function(x) sqrt(sum(x^2))
norminf <- function(x) max(abs(x))

cosine_similarity <- dot_product / (norm2(state_a) * norm2(state_b))

W <- matrix(
  c(
    1.0, 0.0, 0.0,
    0.0, 0.5, 0.0,
    0.0, 0.0, 8.0
  ),
  nrow = 3,
  byrow = TRUE
)

weighted_inner_product <- as.numeric(t(state_a) %*% W %*% state_b)
weighted_distance <- sqrt(as.numeric(t(difference) %*% W %*% difference))

audit_record <- data.frame(
  system_name = "three_indicator_state_space_geometry_audit",
  state_a = paste(round(state_a, 6), collapse = ","),
  state_b = paste(round(state_b, 6), collapse = ","),
  difference_vector = paste(round(difference, 6), collapse = ","),
  dot_product = dot_product,
  cosine_similarity = cosine_similarity,
  weighted_inner_product = weighted_inner_product,
  norm_1 = norm1(difference),
  norm_2 = norm2(difference),
  norm_inf = norminf(difference),
  euclidean_distance = norm2(difference),
  weighted_distance = weighted_distance,
  interpretation_warning = paste(
    "State-space distance depends on units, scaling, norm choice, and weights.",
    "Weighted distances require documented domain justification."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_state_space_geometry_audit.csv", row.names = FALSE)
print(audit_record)
