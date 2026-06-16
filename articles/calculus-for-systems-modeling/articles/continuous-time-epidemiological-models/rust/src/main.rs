fn r0_value(beta: f64, gamma: f64) -> f64 {
    beta / gamma
}
fn doubling_time(growth: f64) -> f64 {
    if growth <= 0.0 { f64::INFINITY } else { std::f64::consts::LN_2 / growth }
}

fn main() {
    println!("scenario_name,model_type,reproduction_number,doubling_time,warning");
    println!("baseline_sir,SIR,{:.6},{:.6},baseline_model_assumptions", r0_value(0.32,0.10), doubling_time(0.22));
    println!("reduced_transmission_sir,SIR,{:.6},{:.6},reduced_transmission_must_have_mechanism", r0_value(0.22,0.10), doubling_time(0.12));
}
