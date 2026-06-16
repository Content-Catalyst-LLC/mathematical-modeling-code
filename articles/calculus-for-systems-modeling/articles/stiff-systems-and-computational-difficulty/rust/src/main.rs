fn exact_solution(t: f64, y0: f64, lambda: f64) -> f64 { y0 * (lambda * t).exp() }
fn explicit_value(y0: f64, lambda: f64, h: f64, stop_time: f64) -> f64 {
    let steps = (stop_time / h).round() as usize;
    let amp = 1.0 + h * lambda;
    let mut y = y0;
    for _ in 0..steps { y *= amp; }
    y
}
fn implicit_value(y0: f64, lambda: f64, h: f64, stop_time: f64) -> f64 {
    let steps = (stop_time / h).round() as usize;
    let amp = 1.0 / (1.0 - h * lambda);
    let mut y = y0;
    for _ in 0..steps { y *= amp; }
    y
}
fn main() {
    let y0 = 1.0;
    let lambda = -50.0;
    let stop_time = 1.0;
    let exact_final = exact_solution(stop_time, y0, lambda);
    println!("step_size,eigenvalue,method,amplification_factor,stability_status,final_value,exact_final_value,absolute_error,warning");
    for h in [0.1, 0.05, 0.025, 0.01] {
        let ev = explicit_value(y0, lambda, h, stop_time);
        let eamp = (1.0 + h * lambda).abs();
        let iv = implicit_value(y0, lambda, h, stop_time);
        let iamp = (1.0 / (1.0 - h * lambda)).abs();
        println!("{:.6},{:.6},explicit_euler,{:.12},{},{:.12},{:.12},{:.12},Explicit methods may require very small steps on stiff systems.",
            h, lambda, eamp, if eamp <= 1.0 {"stable_for_test_problem"} else {"unstable_for_test_problem"}, ev, exact_final, (ev - exact_final).abs());
        println!("{:.6},{:.6},implicit_euler,{:.12},{},{:.12},{:.12},{:.12},Implicit stability does not remove accuracy review.",
            h, lambda, iamp, if iamp <= 1.0 {"stable_for_test_problem"} else {"unstable_for_test_problem"}, iv, exact_final, (iv - exact_final).abs());
    }
}
