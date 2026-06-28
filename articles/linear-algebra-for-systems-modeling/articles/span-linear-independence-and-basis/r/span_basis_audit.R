candidate_matrix <- matrix(
  c(
    1.0, 0.0, 0.5,
    0.0, 1.0, 0.5,
    0.0, 0.0, 1.0
  ),
  nrow = 3,
  byrow = TRUE
)

ambient_dimension <- nrow(candidate_matrix)
vector_count <- ncol(candidate_matrix)
rank_value <- qr(candidate_matrix)$rank

spans_ambient_space <- rank_value == ambient_dimension
linearly_independent <- rank_value == vector_count
is_basis_for_ambient_space <- spans_ambient_space && linearly_independent

audit_record <- data.frame(
  vector_set_name = "candidate_system_basis",
  ambient_dimension = ambient_dimension,
  vector_count = vector_count,
  rank = rank_value,
  spans_ambient_space = spans_ambient_space,
  linearly_independent = linearly_independent,
  is_basis_for_ambient_space = is_basis_for_ambient_space,
  modeling_role = "Candidate basis vectors for a simplified system representation.",
  interpretation_warning = paste(
    "A basis for the mathematical representation is not automatically",
    "an adequate basis for the real system."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)

write.csv(
  audit_record,
  "outputs/tables/r_span_basis_audit.csv",
  row.names = FALSE
)

print(audit_record)
