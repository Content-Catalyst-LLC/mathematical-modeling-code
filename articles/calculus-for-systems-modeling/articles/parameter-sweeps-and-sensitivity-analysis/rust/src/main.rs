fn logistic(t: f64, x0: f64, r: f64, k: f64) -> f64 {
    k / (1.0 + ((k - x0) / x0) * (-r * t).exp())
}
fn main() {
    let rates = [0.18, 0.25, 0.35, 0.45, 0.55];
    let caps = [80.0, 100.0, 125.0, 150.0];
    println!("growth_rate,carrying_capacity,initial_value,stop_time,final_value,output_metric,warning");
    for r in rates {
        for k in caps {
            println!("{:.6},{:.6},10.000000,20.000000,{:.12},final_state_value,Sweep results depend on tested ranges baseline assumptions and model structure.", r, k, logistic(20.0, 10.0, r, k));
        }
    }
}
