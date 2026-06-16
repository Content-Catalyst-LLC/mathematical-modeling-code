fn signal(x: f64) -> f64 {
    x.sin() + 0.1 * x * x
}

fn true_derivative(x: f64) -> f64 {
    x.cos() + 0.2 * x
}

fn main() {
    let start = 0.0_f64;
    let stop = 10.0_f64;
    let h = 0.1_f64;
    let n = ((stop - start) / h).round() as usize;
    let xs: Vec<f64> = (0..=n).map(|i| start + i as f64 * h).collect();
    let values: Vec<f64> = xs.iter().map(|&x| signal(x)).collect();

    println!("index,x,value,true_derivative,forward_difference,backward_difference,central_difference,central_absolute_error,step_size,warning");
    for i in 0..=n {
        let forward = if i < n { (values[i+1] - values[i]) / h } else { f64::NAN };
        let backward = if i > 0 { (values[i] - values[i-1]) / h } else { f64::NAN };
        let central = if i > 0 && i < n { (values[i+1] - values[i-1]) / (2.0*h) } else { f64::NAN };
        let err = if i > 0 && i < n { (central - true_derivative(xs[i])).abs() } else { f64::NAN };
        println!("{},{:.6},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.6},Numerical derivatives depend on step size formula choice boundary handling smoothness and noise.",
            i, xs[i], values[i], true_derivative(xs[i]), forward, backward, central, err, h);
    }
}
