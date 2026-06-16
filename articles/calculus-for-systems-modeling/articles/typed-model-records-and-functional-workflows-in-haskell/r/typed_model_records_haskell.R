model_output_path <- "outputs/tables/typed_model_output.csv"
diagnostics_path <- "outputs/tables/diagnostics.csv"

if (!file.exists(model_output_path) || !file.exists(diagnostics_path)) {
  stop("Run the Python or Haskell export workflow before reading typed model outputs.")
}

model_output <- read.csv(model_output_path)
diagnostics <- read.csv(diagnostics_path)

review_summary <- data.frame(
  model_use = model_output$model_use,
  final_time = model_output$final_time,
  final_stock = model_output$final_stock,
  diagnostic_count = nrow(diagnostics),
  review_required_count = sum(diagnostics$review_required == TRUE),
  interpretation_warning = model_output$interpretation_warning
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(review_summary, "outputs/tables/r_typed_model_review_summary.csv", row.names = FALSE)

print(review_summary)
print(diagnostics)
