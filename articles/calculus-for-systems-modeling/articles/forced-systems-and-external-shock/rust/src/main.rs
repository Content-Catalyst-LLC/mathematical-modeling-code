fn restoring_rate(x: f64, equilibrium: f64, recovery_rate: f64) -> f64 {
    -recovery_rate * (x - equilibrium)
}

fn impulse_shock(time: f64, shock_time: f64, shock_magnitude: f64) -> f64 {
    if (time - shock_time).abs() < 1e-12 { shock_magnitude } else { 0.0 }
}

fn main() {
    let mut baseline = 100.0;
    let mut forced = 100.0;
    let equilibrium = 100.0;
    let recovery_rate = 0.15;
    let shock_time = 10.0;
    let shock_magnitude = -30.0;
    let dt = 0.1;
    println!("step,time,baseline_state,forced_state,shock_value,absolute_deviation,warning");
    for step in 0..=300 {
        let time = step as f64 * dt;
        let shock = impulse_shock(time, shock_time, shock_magnitude);
        println!("{},{:.6},{:.6},{:.6},{:.6},{:.6},Shock response depends on forcing form timing magnitude recovery rate and numerical step size.", step, time, baseline, forced, shock, (forced-baseline).abs());
        baseline = baseline + dt * restoring_rate(baseline, equilibrium, recovery_rate);
        if shock != 0.0 { forced += shock; }
        forced = forced + dt * restoring_rate(forced, equilibrium, recovery_rate);
    }
}
