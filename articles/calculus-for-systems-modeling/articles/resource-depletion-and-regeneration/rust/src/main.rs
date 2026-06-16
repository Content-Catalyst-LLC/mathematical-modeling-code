fn logistic_regeneration(stock: f64, r: f64, k: f64) -> f64 {
    f64::max(0.0, r * stock * (1.0 - stock / k))
}

fn main() {
    let mut stock = 600.0;
    let harvest = 35.0;
    let dt = 0.1;
    let mut cumulative = 0.0;
    for _ in 0..800 {
        let extraction = f64::min(stock, harvest * dt);
        let growth = logistic_regeneration(stock, 0.18, 1000.0) * dt;
        stock = f64::max(0.0, stock + growth - extraction);
        cumulative += extraction;
    }
    println!("scenario_name,resource_type,final_stock,cumulative_extraction,warning");
    println!("renewable_precautionary_harvest,renewable_logistic,{:.6},{:.6},precautionary_harvest", stock, cumulative);
}
