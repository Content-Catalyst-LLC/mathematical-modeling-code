fn equilibrium(input: f64, loss: f64) -> f64 { input / loss }
fn rate_law(y: f64, input: f64, loss: f64) -> f64 { input - loss*y }
fn analytical(t: f64, y0: f64, input: f64, loss: f64) -> f64 {
    let eq = equilibrium(input, loss);
    eq + (y0 - eq) * (-loss*t).exp()
}
fn main() {
    let y0 = 20.0;
    let mut y = 20.0;
    let input = 12.0;
    let loss = 0.4;
    let dt = 0.1;
    let eq = equilibrium(input, loss);
    println!("scenario,time,analytical_state,euler_state,absolute_error,input_rate,loss_rate,equilibrium,initial_state,method,warning");
    for n in 0..=100 {
        let t = n as f64 * dt;
        let a = analytical(t, y0, input, loss);
        println!("input_loss_balance,{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},analytical_vs_explicit_euler,Assumes constant input and proportional loss.", t, a, y, (a-y).abs(), input, loss, eq, y0);
        y += dt * rate_law(y, input, loss);
    }
}
