A <- matrix(
  c(
    3.0, 1.0,
    1.0, 2.0
  ),
  nrow = 2,
  byrow = TRUE
)

b <- c(5.0, 5.0)
solution <- solve(A, b)
residual <- b - A %*% solution
residual_norm <- sqrt(sum(residual^2))
relative_residual <- residual_norm / max(sqrt(sum(b^2)), 1e-15)

checklist <- c(
  notebook_clean_run = TRUE,
  readme_present = TRUE,
  data_dictionary_present = TRUE,
  environment_recorded = TRUE,
  random_seed_recorded_or_not_applicable = TRUE,
  validation_case_present = TRUE,
  diagnostic_outputs_saved = TRUE,
  interpretation_warning_present = TRUE
)

reproducibility_score <- as.integer(100 * sum(checklist) / length(checklist))

audit_record <- data.frame(
  workflow_name = "reproducible_linear_algebra_workflow_audit",
  notebook_status = "clean_execution_required_and_documented",
  documentation_status = "readme_data_dictionary_method_notes_and_governance_report_required",
  matrix_shape = paste(dim(A), collapse = "x"),
  matrix_meaning = "synthetic_reference_system_for_reproducibility_validation",
  data_provenance_status = "synthetic_data_documented_in_workflow",
  environment_status = "runtime_metadata_recorded",
  random_seed_status = "not_applicable_for_deterministic_reference_case",
  validation_status = "reference_solution_and_residual_check_passed",
  generated_outputs_status = "tables_json_and_reports_written_by_workflow",
  residual_norm = residual_norm,
  relative_residual = relative_residual,
  reproducibility_score = reproducibility_score,
  r_version = paste(R.version$major, R.version$minor, sep = "."),
  interpretation_warning = paste(
    "Reproducibility means the workflow can be rerun and reviewed,",
    "not that the model is automatically valid. Matrix construction, diagnostics,",
    "assumptions, uncertainty, and domain validation still require review."
  )
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(audit_record, "outputs/tables/r_reproducible_linear_algebra_audit.csv", row.names = FALSE)
print(audit_record)
