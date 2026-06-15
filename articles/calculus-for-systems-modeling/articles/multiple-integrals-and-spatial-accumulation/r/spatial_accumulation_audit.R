exposure_field <- function(x, y) {
  10 + 2 * x + 0.5 * y^2
}

population_density <- function(x, y) {
  100 + 10 * y + 5 * sin(x)
}

in_region <- function(x, y) {
  x^2 + y^2 <= 9
}

compute_spatial_accumulation <- function(step, scenario) {
  xs <- seq(-3, 3, by = step)
  ys <- seq(-3, 3, by = step)
  cell_area <- step^2
  cells <- 0
  total_density <- 0
  total_population <- 0
  population_burden <- 0

  for (x in xs) {
    for (y in ys) {
      if (in_region(x, y)) {
        exposure <- exposure_field(x, y)
        population <- population_density(x, y)
        cells <- cells + 1
        total_density <- total_density + exposure * cell_area
        total_population <- total_population + population * cell_area
        population_burden <- population_burden + exposure * population * cell_area
      }
    }
  }

  total_area <- cells * cell_area
  area_weighted_average <- total_density / total_area
  population_weighted_average_exposure <- population_burden / total_population
  warning <- ifelse(step > 0.5, "Grid resolution is coarse; spatial accumulation may smooth local variation.", "Synthetic grid audit; region mask, cell area, and units should be documented.")

  data.frame(
    scenario = scenario,
    cells_in_region = cells,
    cell_area = cell_area,
    total_area = total_area,
    total_density_accumulation = total_density,
    area_weighted_average = area_weighted_average,
    population_weighted_burden = population_burden,
    population_total = total_population,
    population_weighted_average_exposure = population_weighted_average_exposure,
    warning = warning
  )
}

results <- rbind(
  compute_spatial_accumulation(1.0, "coarse_grid"),
  compute_spatial_accumulation(0.5, "medium_grid"),
  compute_spatial_accumulation(0.25, "fine_grid")
)

dir.create("outputs/tables", recursive = TRUE, showWarnings = FALSE)
write.csv(results, "outputs/tables/r_spatial_accumulation_audit.csv", row.names = FALSE)
print(results)
