fn delay_function(u: f64) -> f64 {
    if u >= 1.0 { 999.0 } else { 1.0 * (1.0 + 0.8 * (u / (1.0 - u))) }
}

fn main() {
    let arrivals = [75.0, 95.0, 115.0];
    let names = ["baseline_spare_capacity","near_capacity_operation","over_capacity_backlog"];
    println!("scenario_name,system_type,utilization,delay_warning");
    for i in 0..arrivals.len() {
        let u = arrivals[i] / 100.0;
        println!("{},queue_capacity,{:.6},{:.6}", names[i], u, delay_function(u.min(0.999)));
    }
}
