fn geometric_power_series(x: f64, n_terms: usize) -> f64 {
    let mut total = 0.0;
    for n in 0..n_terms {
        total += x.powi(n as i32);
    }
    total
}

fn main() {
    let cases = vec![(0.25_f64, 5_usize), (0.75_f64, 20_usize), (1.25_f64, 10_usize)];
    println!("function_name,center,x_value,n_terms,partial_sum,reference_value,absolute_error,convergence_status,warning");

    for (x, n_terms) in cases {
        let partial = geometric_power_series(x, n_terms);
        if x.abs() < 1.0 {
            let reference = 1.0 / (1.0 - x);
            println!("1/(1-x),0.0,{:.12},{},{:.12},{:.12},{:.12},inside radius of convergence,", x, n_terms, partial, reference, (reference-partial).abs());
        } else {
            println!("1/(1-x),0.0,{:.12},{},{:.12},,,outside radius of convergence,Power series does not converge for this x value.", x, n_terms, partial);
        }
    }
}
