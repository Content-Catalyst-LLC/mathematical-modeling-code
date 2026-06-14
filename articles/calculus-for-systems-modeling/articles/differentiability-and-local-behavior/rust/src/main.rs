fn smooth_response(x: f64) -> f64 {
    (0.2 * x).exp()
}

fn kink_response(x: f64) -> f64 {
    x.abs()
}

fn forward_difference(f: fn(f64) -> f64, x: f64, h: f64) -> f64 {
    (f(x + h) - f(x)) / h
}

fn backward_difference(f: fn(f64) -> f64, x: f64, h: f64) -> f64 {
    (f(x) - f(x - h)) / h
}

fn central_difference(f: fn(f64) -> f64, x: f64, h: f64) -> f64 {
    (f(x + h) - f(x - h)) / (2.0 * h)
}

fn emit(name: &str, f: fn(f64) -> f64, x0: f64) {
    let h_values = [1.0, 0.5, 0.25, 0.125, 0.0625];

    for h in h_values {
        let fwd = forward_difference(f, x0, h);
        let bwd = backward_difference(f, x0, h);
        let cen = central_difference(f, x0, h);
        let gap = (fwd - bwd).abs();
        println!("{},{:.6},{:.6},{:.12},{:.12},{:.12},{:.12},{}",
            name, x0, h, fwd, bwd, cen, gap, gap > 0.5);
    }
}

fn main() {
    println!("function_name,x0,h,forward,backward,central,one_sided_gap,kink_flag");
    emit("smooth_exp_response", smooth_response, 5.0);
    emit("kink_abs_response", kink_response, 0.0);
}
