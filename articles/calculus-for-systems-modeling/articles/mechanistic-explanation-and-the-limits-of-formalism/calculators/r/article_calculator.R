args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <mechanism-score|formalism-risk> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "mechanism-score") {
  entities <- as.integer(get_arg(2, "1"))
  activities <- as.integer(get_arg(3, "1"))
  relations <- as.integer(get_arg(4, "1"))
  evidence <- as.integer(get_arg(5, "0"))
  scope <- as.integer(get_arg(6, "1"))
  score <- round(100 * sum(c(entities, activities, relations, evidence, scope)) / 5)
  status <- ifelse(score >= 80, "strong", ifelse(score >= 50, "partial", "weak"))
  write_result("r_mechanism_score", data.frame(calculator=cmd, score=score, status=status, warning="A score is a review aid not proof of explanatory validity."))
} else if (cmd == "formalism-risk") {
  parameter_meaning <- as.integer(get_arg(2, "0"))
  evidence_link <- as.integer(get_arg(3, "0"))
  validation_scope <- as.integer(get_arg(4, "1"))
  claim_boundary <- as.integer(get_arg(5, "0"))
  missing <- 4 - sum(c(parameter_meaning, evidence_link, validation_scope, claim_boundary))
  risk <- ifelse(missing >= 3, "high", ifelse(missing >= 1, "moderate", "low"))
  write_result("r_formalism_risk", data.frame(calculator=cmd, missing_items=missing, risk=risk, warning="Formal consistency does not guarantee explanatory validity."))
} else {
  stop(paste("Unknown command:", cmd))
}
