fn system_response(x: f64) -> f64 {
    (0.2 * x).exp()
}

fn exact_derivative(x: f64) -> f64 {
    0.2 * (0.2 * x).exp()
}

fn difference_quotient(x: f64, h: f64) -> f64 {
    (system_response(x + h) - system_response(x)) / h
}

fn main() {
    let x = 5.0;
    let exact = exact_derivative(x);
    let h_values = [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001];

    println!("function_name,x,h,estimate,exact_value,absolute_error");
    for h in h_values {
        let estimate = difference_quotient(x, h);
        println!("exp(0.2x),{:.6},{:.6},{:.12},{:.12},{:.12}", x, h, estimate, exact, (estimate - exact).abs());
    }
}
