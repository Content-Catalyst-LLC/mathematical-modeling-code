fn main() {
    let initial_state: f64 = 80.0;
    let target: f64 = 100.0;
    let adjustment_rate: f64 = 0.2;
    let delay: f64 = 5.0;
    let dt: f64 = 0.1;
    let steps: i32 = 300;
    let delay_steps: i32 = (delay / dt).round() as i32;
    let mut states: Vec<f64> = vec![initial_state];

    println!("step,time,current_state,delayed_state,derivative_value,target,absolute_gap,warning");
    for step in 0..=steps {
        let time = step as f64 * dt;
        let current = *states.last().unwrap();
        let delayed_index = step - delay_steps;
        let delayed = if delayed_index < 0 { initial_state } else { states[delayed_index as usize] };
        let derivative = adjustment_rate * (target - delayed);
        println!("{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},Delayed adjustment depends on delay length history function time step and feedback strength.",
            step, time, current, delayed, derivative, target, (current-target).abs());
        states.push(current + dt * derivative);
    }
}
