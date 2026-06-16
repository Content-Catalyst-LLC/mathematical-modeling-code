fn logistic(t: f64, x0: f64, r: f64, k: f64) -> f64 {
    k / (1.0 + ((k - x0) / x0) * (-r * t).exp())
}
fn main() {
    let times = [0.0,2.0,4.0,6.0,8.0,10.0,12.0];
    let observed = [10.0,17.5,29.2,44.1,60.5,74.0,83.2];
    let rates = [0.22,0.26,0.30,0.34,0.38,0.42];
    let caps = [85.0,95.0,105.0,115.0,125.0];
    println!("growth_rate,carrying_capacity,loss,mean_absolute_residual,max_absolute_residual,warning");
    for r in rates {
        for k in caps {
            let mut loss = 0.0;
            let mut abs_sum = 0.0;
            let mut max_abs = 0.0;
            for i in 0..times.len() {
                let pred = logistic(times[i], 10.0, r, k);
                let res: f64 = observed[i] - pred;
                let ar = res.abs();
                loss += res * res;
                abs_sum += ar;
                if ar > max_abs { max_abs = ar; }
            }
            println!("{:.6},{:.6},{:.12},{:.12},{:.12},Calibration fit does not prove model validity validation and sensitivity review remain required.", r, k, loss, abs_sum / times.len() as f64, max_abs);
        }
    }
}
