fn main() {
    let (alpha, beta, gamma, delta) = (0.6, 0.02, 0.5, 0.01);
    let (mut x, mut y, dt) = (40.0, 9.0, 0.02);
    for _ in 0..4000 {
        let dx = alpha * x - beta * x * y;
        let dy = delta * x * y - gamma * y;
        x = f64::max(0.0, x + dt * dx);
        y = f64::max(0.0, y + dt * dy);
    }
    println!("scenario_name,model_type,final_prey,final_predator,warning");
    println!("classic_lotka_volterra,lotka_volterra,{:.6},{:.6},mass_action_baseline", x, y);
}
