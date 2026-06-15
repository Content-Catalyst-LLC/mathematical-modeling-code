fn forcing_function(t: f64, amplitude: f64, frequency: f64) -> f64 { amplitude * (frequency*t).cos() }

fn acceleration(x: f64, v: f64, t: f64, damping: f64, natural: f64, force_amp: f64, force_freq: f64) -> f64 {
    forcing_function(t, force_amp, force_freq) - 2.0*damping*natural*v - natural*natural*x
}

fn simulate(scenario: &str, damping: f64, force_amp: f64) {
    let mut x = 1.0;
    let mut v = 0.0;
    let natural = 1.0;
    let force_freq = 1.0;
    let dt = 0.02;
    for n in 0..=500 {
        let t = n as f64 * dt;
        let a = acceleration(x, v, t, damping, natural, force_amp, force_freq);
        let force = forcing_function(t, force_amp, force_freq);
        println!("{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},explicit_euler_first_order_system,Explicit Euler is transparent but can distort oscillatory systems if the step size is too large.",
            scenario, t, x, v, a, damping, natural, force);
        v += dt*a;
        x += dt*v;
    }
}

fn main() {
    println!("scenario,time,position,velocity,acceleration,damping_ratio,natural_frequency,forcing,method,warning");
    simulate("underdamped_unforced", 0.2, 0.0);
    simulate("forced_near_resonance", 0.1, 0.2);
}
