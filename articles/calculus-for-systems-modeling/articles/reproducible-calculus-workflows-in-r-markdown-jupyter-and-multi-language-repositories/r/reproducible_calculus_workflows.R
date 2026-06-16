workflow_outputs <- data.frame(
  artifact_name = c(
    "parameter_records",
    "sensitivity_table",
    "calibration_report",
    "diagnostics_json",
    "governance_queue"
  ),
  artifact_type = c("csv", "csv", "markdown", "json", "markdown"),
  path = c(
    "data/parameter_records.csv",
    "outputs/tables/sensitivity_table.csv",
    "outputs/reports/calibration_report.md",
    "outputs/json/diagnostics.json",
    "outputs/reports/governance_queue.md"
  ),
  source_or_generated = c("source", "generated", "generated", "generated", "generated"),
  review_role = c(
    "documents parameter values and units",
    "records parameter sensitivity evidence",
    "summarizes calibration and residual diagnostics",
    "stores structured warning and status records",
    "collects review items for unresolved issues"
  ),
  warning = c(
    "Parameter records do not prove empirical correctness.",
    "Sensitivity evidence depends on tested ranges.",
    "Calibration is not validation.",
    "Diagnostics should remain attached to outputs.",
    "Governance queues support judgment but do not replace it."
  )
)

review_summary <- data.frame(
  workflow_name = "r_markdown_style_calculus_report",
  output_count = nrow(workflow_outputs),
  generated_output_count = sum(workflow_outputs$source_or_generated == "generated"),
  review_required = TRUE,
  interpretation_warning = "Executable reports support reproducibility only when outputs can be regenerated from source."
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(workflow_outputs, "outputs/tables/r_workflow_output_register.csv", row.names = FALSE)
write.csv(review_summary, "outputs/tables/r_workflow_review_summary.csv", row.names = FALSE)

print(workflow_outputs)
print(review_summary)
