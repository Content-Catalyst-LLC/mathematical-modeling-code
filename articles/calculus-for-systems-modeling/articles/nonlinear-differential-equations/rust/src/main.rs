fn logistic_rate(x: f64, growth: f64, carrying: f64) -> f64 { growth*x*(1.0 - x/carrying) }
fn bistable_rate(x: f64, threshold: f64) -> f64 { x*(1.0-x)*(x-threshold) }

fn main() {
    println!("scenario,time,state,rate,parameter_a,parameter_b,parameter_c,method,warning");
    let dt = 0.05;
    let mut x = 10.0;
    for n in 0..=300 {
        let t = n as f64 * dt;
        let r = logistic_rate(x, 0.6, 100.0);
        println!("logistic_growth,{:.6},{:.6},{:.6},{:.6},{:.6},0.000000,explicit_euler,Logistic growth assumes a fixed carrying capacity and smooth density limitation.", t, x, r, 0.6, 100.0);
        x += dt*r;
    }
    x = 0.35;
    for n in 0..=300 {
        let t = n as f64 * dt;
        let r = bistable_rate(x, 0.4);
        println!("bistable_threshold,{:.6},{:.6},{:.6},{:.6},0.000000,0.000000,explicit_euler,Threshold behavior is illustrative and should not be interpreted without evidence for the threshold.", t, x, r, 0.4);
        x += dt*r;
    }
}
