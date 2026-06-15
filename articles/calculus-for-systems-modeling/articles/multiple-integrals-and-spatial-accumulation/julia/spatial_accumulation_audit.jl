exposure_field(x, y) = 10.0 + 2.0*x + 0.5*y*y
population_density(x, y) = 100.0 + 10.0*y + 5.0*sin(x)
in_region(x, y) = x*x + y*y <= 9.0

function compute_spatial_accumulation(step, scenario)
    xs = collect(-3.0:step:3.0)
    ys = collect(-3.0:step:3.0)
    cell_area = step^2
    cells = 0
    total_density = 0.0
    total_population = 0.0
    population_burden = 0.0

    for x in xs
        for y in ys
            if in_region(x, y)
                exposure = exposure_field(x, y)
                population = population_density(x, y)
                cells += 1
                total_density += exposure * cell_area
                total_population += population * cell_area
                population_burden += exposure * population * cell_area
            end
        end
    end

    total_area = cells * cell_area
    area_average = total_density / total_area
    population_average = population_burden / total_population
    warning = step > 0.5 ? "Grid resolution is coarse; spatial accumulation may smooth local variation." : "Synthetic grid audit; region mask, cell area, and units should be documented."
    return scenario, cells, cell_area, total_area, total_density, area_average, population_burden, total_population, population_average, warning
end

println("scenario,cells_in_region,cell_area,total_area,total_density_accumulation,area_weighted_average,population_weighted_burden,population_total,population_weighted_average_exposure,warning")
for case in [(1.0, "coarse_grid"), (0.5, "medium_grid"), (0.25, "fine_grid")]
    row = compute_spatial_accumulation(case[1], case[2])
    println(join(row, ","))
end
