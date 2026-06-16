args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <assumption-risk|parameter-evidence> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }
risk_label <- function(score) ifelse(score >= 3, "high", ifelse(score >= 1, "moderate", "low"))

if (cmd == "assumption-risk") {
  hidden_assumptions <- as.integer(get_arg(2, "2"))
  normative_assumptions <- as.integer(get_arg(3, "1"))
  solver_undocumented <- as.integer(get_arg(4, "1"))
  score <- sum(c(hidden_assumptions, normative_assumptions, solver_undocumented))
  write_result("r_assumption_risk", data.frame(calculator=cmd, risk_score=score, risk=risk_label(score), warning="Hidden assumptions can create false confidence."))
} else if (cmd == "parameter-evidence") {
  has_unit <- as.integer(get_arg(2, "1"))
  has_source <- as.integer(get_arg(3, "1"))
  has_range <- as.integer(get_arg(4, "0"))
  has_uncertainty <- as.integer(get_arg(5, "0"))
  score <- sum(c(has_unit, has_source, has_range, has_uncertainty))
  status <- ifelse(score == 4, "complete", ifelse(score >= 2, "partial", "weak"))
  write_result("r_parameter_evidence", data.frame(calculator=cmd, evidence_score=score, status=status, warning="A parameter value without evidence status is incomplete."))
} else {
  stop(paste("Unknown command:", cmd))
}
