fn continuous_future_value(v0: f64, r: f64, t: f64) -> f64 {
    v0 * (r * t).exp()
}

fn continuous_present_value(fv: f64, r: f64, t: f64) -> f64 {
    fv * (-r * t).exp()
}

fn main() {
    println!("scenario_name,model_type,final_value,present_value,warning");
    println!("continuous_compounding_case,future_value,{:.6},1000.000000,continuous_compounding", continuous_future_value(1000.0, 0.05, 30.0));
    println!("discounted_future_value,present_value,5000.000000,{:.6},discounting", continuous_present_value(5000.0, 0.05, 30.0));
}
