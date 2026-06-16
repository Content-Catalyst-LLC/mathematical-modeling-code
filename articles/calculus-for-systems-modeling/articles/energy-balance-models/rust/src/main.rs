fn equilibrium_temperature(forcing: f64, feedback: f64) -> f64 { forcing / feedback }
fn adjustment_time(heat_capacity: f64, feedback: f64) -> f64 { heat_capacity / feedback }
fn absorbed_solar(solar_constant: f64, albedo: f64) -> f64 { solar_constant * (1.0 - albedo) / 4.0 }
fn main() {
    println!("scenario_name,model_type,equilibrium_temperature,adjustment_time,absorbed_solar,warning");
    println!("baseline_one_layer,one_layer,{:.6},{:.6},{:.6},boundaries_and_feedback_must_be_documented", equilibrium_temperature(3.7,1.2), adjustment_time(10.0,1.2), absorbed_solar(1361.0,0.30));
    println!("stronger_feedback,one_layer,{:.6},{:.6},{:.6},feedback_strength_changes_response", equilibrium_temperature(3.7,1.8), adjustment_time(10.0,1.8), absorbed_solar(1361.0,0.30));
}
