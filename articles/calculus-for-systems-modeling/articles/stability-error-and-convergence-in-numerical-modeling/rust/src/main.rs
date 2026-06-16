fn exact_solution(t: f64, y0: f64, k: f64) -> f64 { y0 * (-k * t).exp() }
fn rate_function(_t: f64, y: f64, k: f64) -> f64 { -k * y }
fn rk4_step(t: f64, y: f64, h: f64, k: f64) -> f64 {
    let k1 = rate_function(t, y, k);
    let k2 = rate_function(t + h/2.0, y + h*k1/2.0, k);
    let k3 = rate_function(t + h/2.0, y + h*k2/2.0, k);
    let k4 = rate_function(t + h, y + h*k3, k);
    y + (h/6.0) * (k1 + 2.0*k2 + 2.0*k3 + k4)
}
fn simulate(y0: f64, k: f64, h: f64, stop_time: f64) -> f64 {
    let steps = (stop_time / h).round() as usize;
    let mut y = y0;
    for step in 0..steps { y = rk4_step(step as f64 * h, y, h, k); }
    y
}
fn main() {
    let y0 = 100.0;
    let k = 0.35;
    let stop_time = 20.0;
    let exact_final = exact_solution(stop_time, y0, k);
    println!("step_size,steps,solver_method,final_numeric_value,final_exact_value,final_absolute_error,warning");
    for h in [1.0, 0.5, 0.25, 0.125] {
        let numeric = simulate(y0, k, h, stop_time);
        println!("{:.6},{},fixed_step_rk4,{:.12},{:.12},{:.12},Convergence evidence supports numerical reliability not empirical validity.",
            h, (stop_time / h).round() as usize, numeric, exact_final, (numeric - exact_final).abs());
    }
}
