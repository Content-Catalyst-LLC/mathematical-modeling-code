fn exact_solution(t: f64, y0: f64, k: f64) -> f64 {
    y0 * (-k * t).exp()
}

fn main() {
    let y0 = 100.0_f64;
    let k = 0.35_f64;
    let h = 0.1_f64;
    let stop_time = 20.0_f64;
    let steps = (stop_time / h).round() as usize;
    let mut y = y0;
    let multiplier = 1.0 - h * k;
    let status = if multiplier.abs() <= 1.0 { "stable_for_simple_decay" } else { "unstable_risk" };

    println!("step,time,euler_value,exact_value,absolute_error,step_size,stability_multiplier,stability_status,warning");
    for step in 0..=steps {
        let t = step as f64 * h;
        let exact = exact_solution(t, y0, k);
        println!("{},{:.6},{:.12},{:.12},{:.12},{:.6},{:.12},{},Euler estimates depend on time step rate function initial condition stability and accumulated error.",
            step, t, y, exact, (y - exact).abs(), h, multiplier, status);
        y = y + h * (-k * y);
    }
}
