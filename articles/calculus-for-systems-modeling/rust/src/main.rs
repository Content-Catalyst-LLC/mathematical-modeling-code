fn simulate_logistic(initial_state: f64, rate: f64, capacity: f64, dt: f64, steps: usize) -> Vec<f64> {
    let mut state = vec![0.0; steps];
    state[0] = initial_state;

    for i in 1..steps {
        let derivative = rate * state[i - 1] * (1.0 - state[i - 1] / capacity);
        state[i] = state[i - 1] + derivative * dt;
    }

    state
}

fn main() {
    let state = simulate_logistic(10.0, 0.20, 100.0, 0.1, 300);
    println!("Final state: {:.6}", state[state.len() - 1]);
}
