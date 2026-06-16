fn exponential_output(y0: f64, g: f64, t: f64) -> f64 {
    y0 * (g * t).exp()
}

fn main() {
    let rates = [0.01, 0.025, 0.04];
    println!("scenario_name,model_type,growth_rate,final_output,doubling_time,warning");
    for g in rates {
        println!("growth_rate_case,exponential_growth,{:.6},{:.6},{:.6},growth_rate_assumptions_compound", g, exponential_output(100.0, g, 40.0), std::f64::consts::LN_2 / g);
    }
}
