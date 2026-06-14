#[derive(Debug)]
struct Scenario {
    name: &'static str,
    initial_state: f64,
    rate: f64,
    capacity: f64,
    dt: f64,
    steps: usize,
}

fn simulate(s: &Scenario) -> f64 {
    let mut state = s.initial_state;
    for _ in 0..s.steps {
        let derivative = s.rate * state * (1.0 - state / s.capacity);
        state = (state + derivative * s.dt).max(0.0);
    }
    state
}

fn main() {
    let scenarios = [
        Scenario { name: "baseline", initial_state: 10.0, rate: 0.20, capacity: 100.0, dt: 0.1, steps: 300 },
        Scenario { name: "slow_adjustment", initial_state: 10.0, rate: 0.10, capacity: 100.0, dt: 0.1, steps: 300 },
        Scenario { name: "high_capacity", initial_state: 10.0, rate: 0.20, capacity: 140.0, dt: 0.1, steps: 300 },
    ];

    println!("scenario,final_state");
    for s in &scenarios {
        println!("{},{}", s.name, simulate(s));
    }
}
