fn exponential_population(n0: f64, r: f64, t: f64) -> f64 {
    n0 * (r * t).exp()
}

fn logistic_population(n0: f64, r: f64, k: f64, t: f64) -> f64 {
    k / (1.0 + ((k - n0) / n0) * (-r * t).exp())
}

fn main() {
    let n0 = 100.0;
    let r = 0.08;
    let k = 1000.0;
    println!("time,exponential,logistic");
    for t in 0..=40 {
        let tf = t as f64;
        println!("{},{:.6},{:.6}", t, exponential_population(n0, r, tf), logistic_population(n0, r, k, tf));
    }
}
