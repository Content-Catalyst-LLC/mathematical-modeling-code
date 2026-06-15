args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) stop("Usage: Rscript article_calculator.R <rectangle-total|grid-total|population-weighted> ...")
cmd <- args[[1]]
out_dir <- "outputs"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
get_arg <- function(i, default) if (length(args) >= i && nzchar(args[[i]])) args[[i]] else default
write_result <- function(name, df) { write.csv(df, file.path(out_dir, paste0(name, ".csv")), row.names = FALSE); print(df) }

exposure_field <- function(x, y) 10 + 2*x + 0.5*y^2
population_density <- function(x, y) 100 + 10*y + 5*sin(x)
in_region <- function(x, y) x^2 + y^2 <= 9

compute_grid <- function(step) {
  xs <- seq(-3, 3, by = step)
  ys <- seq(-3, 3, by = step)
  cell_area <- step^2
  cells <- 0
  total <- 0
  population_total <- 0
  population_burden <- 0
  for (x in xs) {
    for (y in ys) {
      if (in_region(x, y)) {
        exposure <- exposure_field(x, y)
        population <- population_density(x, y)
        cells <- cells + 1
        total <- total + exposure * cell_area
        population_total <- population_total + population * cell_area
        population_burden <- population_burden + exposure * population * cell_area
      }
    }
  }
  area <- cells * cell_area
  data.frame(cells_in_region=cells, cell_area=cell_area, total_area=area, total_density_accumulation=total, area_weighted_average=total/area, population_total=population_total, population_weighted_burden=population_burden, population_weighted_average_exposure=population_burden/population_total)
}

if (cmd == "rectangle-total") {
  density <- as.numeric(get_arg(2, "12")); width <- as.numeric(get_arg(3, "4")); height <- as.numeric(get_arg(4, "3"))
  write_result("r_rectangle_total", data.frame(calculator=cmd, density=density, width=width, height=height, area=width*height, total=density*width*height))
} else if (cmd == "grid-total") {
  step <- as.numeric(get_arg(2, "0.5"))
  write_result("r_grid_total", cbind(data.frame(calculator=cmd, step=step), compute_grid(step)))
} else if (cmd == "population-weighted") {
  step <- as.numeric(get_arg(2, "0.5"))
  grid <- compute_grid(step)
  write_result("r_population_weighted", data.frame(calculator=cmd, step=step, population_weighted_average_exposure=grid$population_weighted_average_exposure, population_weighted_burden=grid$population_weighted_burden, population_total=grid$population_total))
} else {
  stop(paste("Unknown command:", cmd))
}
