fn simulate_logistic(initial_state: f64, growth_rate: f64, carrying_capacity: f64, time_steps: usize) -> Vec<f64> {
    let mut state = vec![0.0; time_steps];
    state[0] = initial_state;

    for t in 1..time_steps {
        state[t] = state[t - 1] + growth_rate * state[t - 1] * (1.0 - state[t - 1] / carrying_capacity);
    }

    state
}

fn main() {
    let state = simulate_logistic(10.0, 0.18, 100.0, 80);

    println!("Mathematical Modeling CLI");
    println!("Final state: {:.3}", state[state.len() - 1]);
}
