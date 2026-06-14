# Base R workflow for engineering design and safety review.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

tables_dir <- file.path(article_root, "outputs", "tables")
figures_dir <- file.path(article_root, "outputs", "figures")
dir.create(tables_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

register_path <- file.path(tables_dir, "engineering_model_register.csv")
design_path <- file.path(tables_dir, "beam_design_review.csv")

if (!file.exists(register_path) || !file.exists(design_path)) {
  stop("Missing engineering modeling outputs. Run make python first.")
}

register <- read.csv(register_path, stringsAsFactors = FALSE)
designs <- read.csv(design_path, stringsAsFactors = FALSE)

register$engineering_priority <- as.numeric(register$engineering_priority)
designs$safety_factor <- as.numeric(designs$safety_factor)
designs$estimated_mass_kg <- as.numeric(designs$estimated_mass_kg)
designs$max_stress_pa <- as.numeric(designs$max_stress_pa)
designs$stress_margin_pa <- as.numeric(designs$stress_margin_pa)

register <- register[order(-register$engineering_priority), ]
designs <- designs[order(-designs$safety_factor), ]

pass_values <- tolower(as.character(designs$passes_stress_constraint))
failed_count <- sum(pass_values %in% c("false", "0", "no"))

summary_table <- data.frame(
  mean_safety_factor = mean(designs$safety_factor),
  min_safety_factor = min(designs$safety_factor),
  max_safety_factor = max(designs$safety_factor),
  failed_design_count = failed_count,
  design_count = nrow(designs)
)

write.csv(
  register,
  file.path(tables_dir, "r_engineering_model_review_queue.csv"),
  row.names = FALSE
)

write.csv(
  designs,
  file.path(tables_dir, "r_beam_design_ranking.csv"),
  row.names = FALSE
)

write.csv(
  summary_table,
  file.path(tables_dir, "r_engineering_design_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "r_beam_safety_factors.png"), width = 1000, height = 700)

barplot(
  designs$safety_factor,
  names.arg = designs$key,
  las = 2,
  ylab = "Safety factor",
  main = "Beam Design Safety Factors"
)

dev.off()

print(register)
print(summary_table)
print(designs)
