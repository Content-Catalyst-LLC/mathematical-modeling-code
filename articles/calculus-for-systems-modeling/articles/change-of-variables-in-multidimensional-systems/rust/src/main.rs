const PI: f64 = std::f64::consts::PI;

fn exposure_cartesian(x: f64, y: f64) -> f64 {
    let r = (x*x + y*y).sqrt();
    20.0 * (-0.4 * r).exp()
}

fn exposure_polar(r: f64, _theta: f64) -> f64 {
    20.0 * (-0.4 * r).exp()
}

fn polar_total(radius: f64, dr: f64, dtheta: f64) -> f64 {
    let mut total = 0.0;
    let mut r = dr / 2.0;
    while r < radius {
        let mut theta = dtheta / 2.0;
        while theta < 2.0 * PI {
            total += exposure_polar(r, theta) * r * dr * dtheta;
            theta += dtheta;
        }
        r += dr;
    }
    total
}

fn cartesian_grid_total(radius: f64, step: f64) -> f64 {
    let mut total = 0.0;
    let n = ((2.0 * radius) / step) as i32;
    for i in 0..=n {
        let x = -radius + (i as f64) * step;
        for j in 0..=n {
            let y = -radius + (j as f64) * step;
            if x*x + y*y <= radius*radius {
                total += exposure_cartesian(x, y) * step * step;
            }
        }
    }
    total
}

fn audit(radius: f64, dr: f64, dtheta: f64, scenario: &str) {
    let p = polar_total(radius, dr, dtheta);
    let c = cartesian_grid_total(radius, dr);
    let diff = (p - c).abs();
    let rel = diff / p.abs().max(1e-12);
    let warning = if dr > 0.5 { "Resolution is coarse; transformed and Cartesian approximations may differ." } else { "Polar Jacobian factor r included; compare domain and resolution assumptions." };
    println!("{},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},dA = r dr dtheta,{}", scenario, radius, dr, dtheta, p, c, diff, rel, warning);
}

fn main() {
    println!("scenario,radius,radial_step,angular_step,polar_total,cartesian_grid_total,absolute_difference,relative_difference,jacobian_rule,warning");
    audit(3.0, 0.5, PI / 24.0, "medium_polar_grid");
    audit(3.0, 0.25, PI / 48.0, "fine_polar_grid");
    audit(3.0, 0.125, PI / 96.0, "very_fine_polar_grid");
}
