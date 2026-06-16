fn rate_function(_t: f64, y: f64, k: f64) -> f64 { -k * y }
fn exact_solution(t: f64, y0: f64, k: f64) -> f64 { y0 * (-k * t).exp() }
fn euler_step(t: f64, y: f64, h: f64, k: f64) -> f64 { y + h * rate_function(t, y, k) }
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
    let mut euler_y = y0;
    let mut rk_y = y0;

    println!("step,time,euler_value,rk4_value,exact_value,euler_absolute_error,rk4_absolute_error,step_size,warning");
    for step in 0..=steps {
        let t = step as f64 * h;
        let exact = exact_solution(t, y0, k);
        println!("{},{:.6},{:.12},{:.12},{:.12},{:.12},{:.12},{:.6},Runge-Kutta estimates depend on rate function step size smoothness stiffness and benchmark comparison.",
            step, t, euler_y, rk_y, exact, (euler_y-exact).abs(), (rk_y-exact).abs(), h);
        euler_y = euler_step(t, euler_y, h, k);
        rk_y = rk4_step(t, rk_y, h, k);
    }
}
