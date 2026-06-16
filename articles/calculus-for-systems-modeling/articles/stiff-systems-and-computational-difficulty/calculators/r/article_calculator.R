args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <explicit-amplification|stiffness-ratio> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

if (cmd == "explicit-amplification") {
  h <- as.numeric(get_arg(2, "0.1"))
  eigenvalue <- as.numeric(get_arg(3, "-50"))
  amp <- abs(1 + h * eigenvalue)
  write_result("r_explicit_amplification", data.frame(calculator=cmd, step_size=h, eigenvalue=eigenvalue, amplification_factor=amp, status=ifelse(amp <= 1, "stable_for_test_problem", "unstable_for_test_problem"), warning="Explicit instability may be numerical artifact rather than real system instability."))
} else if (cmd == "stiffness-ratio") {
  text <- get_arg(2, "-1,-50")
  eigenvalues <- as.numeric(strsplit(text, ",")[[1]])
  mags <- abs(eigenvalues[eigenvalues != 0])
  ratio <- max(mags) / min(mags)
  write_result("r_stiffness_ratio", data.frame(calculator=cmd, eigenvalues=text, stiffness_ratio=ratio, warning="A stiffness ratio is a heuristic diagnostic not a complete proof."))
} else {
  stop(paste("Unknown command:", cmd))
}
