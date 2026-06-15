fn main() {
    let grid_points: usize = 61;
    let steps = 120;
    let diffusivity = 0.08_f64;
    let velocity = 0.4_f64;
    let dx = 1.0_f64;
    let dt = 0.2_f64;
    let d_ratio = diffusivity * dt / (dx * dx);
    let t_ratio = velocity * dt / dx;
    let mut field = vec![0.0_f64; grid_points];
    field[grid_points / 2] = 1.0;

    println!("step,time,center_value,total_mass,max_value,min_value,diffusion_ratio,transport_ratio,warning");
    for step in 0..=steps {
        let total_mass: f64 = field.iter().sum::<f64>() * dx;
        let max_value = field.iter().copied().fold(f64::NEG_INFINITY, f64::max);
        let min_value = field.iter().copied().fold(f64::INFINITY, f64::min);
        println!("{},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},Spatial dynamics depend on field meaning boundary conditions grid spacing time step and numerical stability.",
            step, step as f64 * dt, field[grid_points/2], total_mass, max_value, min_value, d_ratio, t_ratio);

        let mut updated = field.clone();
        for i in 1..grid_points-1 {
            let diffusion_part = d_ratio * (field[i+1] - 2.0 * field[i] + field[i-1]);
            let transport_part = -t_ratio * (field[i] - field[i-1]);
            updated[i] = field[i] + diffusion_part + transport_part;
        }
        updated[0] = 0.0;
        updated[grid_points-1] = 0.0;
        field = updated;
    }
}
