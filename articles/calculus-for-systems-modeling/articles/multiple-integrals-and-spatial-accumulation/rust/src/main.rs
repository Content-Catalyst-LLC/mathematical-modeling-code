fn exposure_field(x: f64, y: f64) -> f64 { 10.0 + 2.0*x + 0.5*y*y }
fn population_density(x: f64, y: f64) -> f64 { 100.0 + 10.0*y + 5.0*x.sin() }
fn in_region(x: f64, y: f64) -> bool { x*x + y*y <= 9.0 }

fn compute(step: f64, scenario: &str) {
    let n = (6.0 / step) as i32;
    let cell_area = step * step;
    let mut cells = 0;
    let mut total_density = 0.0;
    let mut total_population = 0.0;
    let mut population_burden = 0.0;

    for i in 0..=n {
        let x = -3.0 + (i as f64) * step;
        for j in 0..=n {
            let y = -3.0 + (j as f64) * step;
            if in_region(x, y) {
                let exposure = exposure_field(x, y);
                let population = population_density(x, y);
                cells += 1;
                total_density += exposure * cell_area;
                total_population += population * cell_area;
                population_burden += exposure * population * cell_area;
            }
        }
    }

    let total_area = (cells as f64) * cell_area;
    let warning = if step > 0.5 { "Grid resolution is coarse; spatial accumulation may smooth local variation." } else { "Synthetic grid audit; region mask cell area and units should be documented." };
    println!("{},{},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{}", scenario, cells, cell_area, total_area, total_density, total_density/total_area, population_burden, total_population, population_burden/total_population, warning);
}

fn main() {
    println!("scenario,cells_in_region,cell_area,total_area,total_density_accumulation,area_weighted_average,population_weighted_burden,population_total,population_weighted_average_exposure,warning");
    compute(1.0, "coarse_grid");
    compute(0.5, "medium_grid");
    compute(0.25, "fine_grid");
}
