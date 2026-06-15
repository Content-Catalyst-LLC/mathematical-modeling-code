fn height(x: f64, y: f64) -> f64 { 0.1*x*x + 0.05*y*y }
fn scalar_field(_x: f64, _y: f64, z: f64) -> f64 { 1.0 + 0.2*z }
fn vector_field(x: f64, y: f64, _z: f64) -> (f64, f64, f64) { (0.1*x, 0.1*y, 1.0) }
fn normal_area_vector(x: f64, y: f64, step: f64) -> (f64, f64, f64) {
    let area = step*step;
    (-0.2*x*area, -0.1*y*area, area)
}
fn norm3(v: (f64, f64, f64)) -> f64 { (v.0*v.0 + v.1*v.1 + v.2*v.2).sqrt() }
fn dot3(a: (f64, f64, f64), b: (f64, f64, f64)) -> f64 { a.0*b.0 + a.1*b.1 + a.2*b.2 }

fn audit(step: f64, scenario: &str) {
    let n = (2.0 / step) as usize;
    let mut count = 0usize;
    let mut surface_area = 0.0;
    let mut scalar_total = 0.0;
    let mut flux_total = 0.0;
    let mut flux_density_sum = 0.0;
    let mut max_patch = 0.0;

    for i in 0..n {
        let x = -1.0 + i as f64 * step;
        for j in 0..n {
            let y = -1.0 + j as f64 * step;
            let z = height(x,y);
            let area_vector = normal_area_vector(x,y,step);
            let field_vector = vector_field(x,y,z);
            let patch_area = norm3(area_vector);
            let flux = dot3(field_vector, area_vector);
            count += 1;
            surface_area += patch_area;
            scalar_total += scalar_field(x,y,z) * patch_area;
            flux_total += flux;
            flux_density_sum += flux / patch_area.max(1e-12);
            if patch_area > max_patch { max_patch = patch_area; }
        }
    }

    let warning = if step > 0.5 { "Grid step is coarse; curvature and field variation may be undersampled." } else { "Synthetic surface-integral audit; document surface normal units and mesh." };
    println!("{},{:.12},{},{:.12},{:.12},{:.12},{:.12},{:.12},graph z=0.1x^2+0.05y^2,{}", scenario, step, count, surface_area, scalar_total, flux_total, flux_density_sum/(count as f64), max_patch, warning);
}

fn main() {
    println!("scenario,grid_step,patch_count,approximate_surface_area,scalar_surface_integral,vector_flux_integral,average_flux_density,maximum_patch_area,surface_description,warning");
    audit(1.0, "coarse_surface_mesh");
    audit(0.5, "medium_surface_mesh");
    audit(0.25, "fine_surface_mesh");
}
