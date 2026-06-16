fn rate_function(_t: f64, y: f64, k: f64) -> f64 { -k * y }
fn exact_solution(t: f64, y0: f64, k: f64) -> f64 { y0 * (-k * t).exp() }
fn rk4_step(t: f64, y: f64, h: f64, k: f64) -> f64 {
    let k1 = rate_function(t, y, k);
    let k2 = rate_function(t + h / 2.0, y + h * k1 / 2.0, k);
    let k3 = rate_function(t + h / 2.0, y + h * k2 / 2.0, k);
    let k4 = rate_function(t + h, y + h * k3, k);
    y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
}

fn main() {
    let y0 = 100.0_f64;
    let k = 0.35_f64;
    let h = 0.5_f64;
    let stop_time = 20.0_f64;
    let steps = (stop_time / h).round() as usize;
    let mut y = y0;

    println!("step,time,solver_value,exact_value,absolute_error,solver_method,step_size,warning");
    for step in 0..=steps {
        let t = step as f64 * h;
        let exact = exact_solution(t, y0, k);
        println!("{},{:.6},{:.12},{:.12},{:.12},fixed_step_rk4,{:.6},ODE solver outputs depend on equation initial condition method tolerances step size stiffness and diagnostics.",
            step, t, y, exact, (y-exact).abs(), h);
        y = rk4_step(t, y, h, k);
    }
}
