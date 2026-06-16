fn one_box(forcing: f64, feedback: f64, heat_capacity: f64, time: f64) -> f64 {
    let equilibrium = forcing / feedback;
    equilibrium * (1.0 - (-(feedback / heat_capacity) * time).exp())
}

fn main() {
    let forcing = 3.7;
    let c = 8.0;
    println!("time,weak_feedback,baseline_feedback,strong_feedback");
    for t in (0..=100).step_by(10) {
        let tf = t as f64;
        println!("{},{:.6},{:.6},{:.6}", t, one_box(forcing,0.9,c,tf), one_box(forcing,1.2,c,tf), one_box(forcing,1.6,c,tf));
    }
}
