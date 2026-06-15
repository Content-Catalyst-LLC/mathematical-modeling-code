fn logistic_derivative(x: f64, growth: f64, carrying: f64) -> f64 { growth*(1.0 - 2.0*x/carrying) }
fn bistable_rate(x: f64, threshold: f64) -> f64 { x*(1.0-x)*(x-threshold) }
fn numerical_derivative(x: f64, threshold: f64) -> f64 {
    let h = 1e-5;
    (bistable_rate(x+h, threshold) - bistable_rate(x-h, threshold))/(2.0*h)
}
fn classify(d: f64) -> &'static str {
    if d < -1e-8 { "locally_stable" }
    else if d > 1e-8 { "locally_unstable" }
    else { "inconclusive_by_linearization" }
}
fn main() {
    println!("scenario,equilibrium,derivative_value,stability,domain_min,domain_max,warning");
    for eq in [0.0, 100.0] {
        let d = logistic_derivative(eq, 0.6, 100.0);
        println!("logistic_growth,{:.6},{:.6},{},0.000000,100.000000,Logistic stability assumes fixed carrying capacity and smooth density limitation.", eq, d, classify(d));
    }
    for eq in [0.0, 0.4, 1.0] {
        let d = numerical_derivative(eq, 0.4);
        println!("bistable_threshold,{:.6},{:.6},{},0.000000,1.000000,Threshold stability depends on the assumed threshold and domain.", eq, d, classify(d));
    }
}
