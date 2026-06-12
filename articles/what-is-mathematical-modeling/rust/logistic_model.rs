#[derive(Debug, Clone)]
struct LogisticModel {
    name: String,
    initial_state: f64,
    growth_rate: f64,
    carrying_capacity: f64,
    dt: f64,
    steps: usize,
}

fn derivative(x: f64, r: f64, k: f64) -> f64 {
    r * x * (1.0 - x / k)
}

fn rk4_step(x: f64, r: f64, k: f64, dt: f64) -> f64 {
    let k1 = derivative(x, r, k);
    let k2 = derivative(x + 0.5 * dt * k1, r, k);
    let k3 = derivative(x + 0.5 * dt * k2, r, k);
    let k4 = derivative(x + dt * k3, r, k);
    (x + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)).max(0.0)
}

fn simulate(model: &LogisticModel) -> Vec<(usize, f64, f64)> {
    let mut rows = Vec::with_capacity(model.steps + 1);
    let mut x = model.initial_state;
    for step in 0..=model.steps {
        rows.push((step, step as f64 * model.dt, x));
        x = rk4_step(x, model.growth_rate, model.carrying_capacity, model.dt);
    }
    rows
}

fn main() {
    let model = LogisticModel {
        name: "rust_baseline".to_string(),
        initial_state: 10.0,
        growth_rate: 0.35,
        carrying_capacity: 100.0,
        dt: 0.1,
        steps: 160,
    };
    let rows = simulate(&model);
    println!("Rust scenario={} final_state={:.6}", model.name, rows.last().unwrap().2);
}
