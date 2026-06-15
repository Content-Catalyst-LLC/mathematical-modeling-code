fn main() {
    let grid_points: usize = 51;
    let steps = 100;
    let diffusivity = 0.1_f64;
    let dx = 1.0_f64;
    let dt = 0.25_f64;
    let ratio = diffusivity * dt / (dx * dx);
    let mut field = vec![0.0_f64; grid_points];
    field[grid_points / 2] = 1.0;

    println!("step,time,center_value,total_mass,max_value,min_value,stability_ratio,warning");
    for step in 0..=steps {
        let total_mass: f64 = field.iter().sum::<f64>() * dx;
        let max_value = field.iter().copied().fold(f64::NEG_INFINITY, f64::max);
        let min_value = field.iter().copied().fold(f64::INFINITY, f64::min);
        println!("{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},Explicit diffusion schemes require stability checks boundary and grid assumptions shape results.",
            step, step as f64 * dt, field[grid_points/2], total_mass, max_value, min_value, ratio);

        let mut updated = field.clone();
        for i in 1..grid_points-1 {
            updated[i] = field[i] + ratio * (field[i+1] - 2.0 * field[i] + field[i-1]);
        }
        updated[0] = 0.0;
        updated[grid_points-1] = 0.0;
        field = updated;
    }
}
