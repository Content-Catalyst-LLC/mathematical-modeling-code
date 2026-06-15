fn scalar_field(x: f64, y: f64) -> f64 { 20.0 + 2.0*x.sin() + 0.5*y*y }
fn vector_field(x: f64, y: f64) -> (f64, f64) { (-y, x) }
fn vector_magnitude(vx: f64, vy: f64) -> f64 { (vx*vx + vy*vy).sqrt() }

fn audit(step: f64, scenario: &str) {
    let n = (6.0 / step) as i32;
    let mut count = 0;
    let mut scalar_sum = 0.0;
    let mut scalar_min = f64::INFINITY;
    let mut scalar_max = f64::NEG_INFINITY;
    let mut mag_sum = 0.0;
    let mut mag_max = 0.0;

    for i in 0..=n {
        let x = -3.0 + (i as f64) * step;
        for j in 0..=n {
            let y = -3.0 + (j as f64) * step;
            let s = scalar_field(x, y);
            let (vx, vy) = vector_field(x, y);
            let mag = vector_magnitude(vx, vy);
            count += 1;
            scalar_sum += s;
            if s < scalar_min { scalar_min = s; }
            if s > scalar_max { scalar_max = s; }
            mag_sum += mag;
            if mag > mag_max { mag_max = mag; }
        }
    }

    let warning = if step > 0.75 { "Grid resolution is coarse; field structure may be undersampled." } else { "Synthetic field audit; document domain units and interpolation assumptions." };
    println!("{},{:.12},{},{:.12},{:.12},{:.12},{:.12},{:.12},square domain [-3,3] x [-3,3],{}", scenario, step, count, scalar_sum/(count as f64), scalar_min, scalar_max, mag_sum/(count as f64), mag_max, warning);
}

fn main() {
    println!("scenario,grid_step,point_count,scalar_average,scalar_minimum,scalar_maximum,vector_magnitude_average,vector_magnitude_maximum,domain_description,warning");
    audit(1.0, "coarse_grid");
    audit(0.5, "medium_grid");
    audit(0.25, "fine_grid");
}
