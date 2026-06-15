fn logistic_map(x: f64, r: f64) -> f64 {
    r * x * (1.0 - x)
}

fn main() {
    let r = 3.9;
    let mut x_reference = 0.2;
    let mut x_perturbed = 0.2 + 1e-8;
    println!("step,x_reference,x_perturbed,absolute_difference,log_difference,warning");
    for step in 0..=100 {
        let difference = (x_reference - x_perturbed).abs();
        let log_difference = if difference > 0.0 { difference.ln() } else { 0.0 };
        println!("{},{:.12},{:.12},{:.12e},{:.12},Trajectory divergence depends on parameter value initial uncertainty numerical precision and iteration count.", step, x_reference, x_perturbed, difference, log_difference);
        x_reference = logistic_map(x_reference, r);
        x_perturbed = logistic_map(x_perturbed, r);
    }
}
