B <- matrix(c(0.80,0.20,0.35,0.60,0.10,0.50), nrow = 3, byrow = TRUE)
A <- matrix(c(1.10,0.40,0.20,0.25,0.90,0.70), nrow = 2, byrow = TRUE)
product <- A %*% B
reverse_available <- ncol(B) == nrow(A)
noncommutative_warning <- if (reverse_available) "reverse product is dimensionally available but represents a different transformation order" else "reverse product is not dimensionally compatible"
audit_record <- data.frame(
  system_name = "two_stage_demand_to_stress_interaction",
  left_shape = paste(dim(A), collapse = "x"),
  right_shape = paste(dim(B), collapse = "x"),
  product_shape = paste(dim(product), collapse = "x"),
  product_matrix = paste(apply(round(product, 6), 1, paste, collapse = ","), collapse = ";"),
  reverse_product_available = reverse_available,
  noncommutative_warning = noncommutative_warning,
  interaction_interpretation = "B maps demand into intermediate components; A maps intermediate components into stress; AB maps demand into stress through pathways.",
  governance_warning = "Matrix products require transformation order, intermediate-layer meaning, units, and row-column alignment review."
)
dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_matrix_product_interaction_audit.csv", row.names = FALSE)
print(audit_record)
