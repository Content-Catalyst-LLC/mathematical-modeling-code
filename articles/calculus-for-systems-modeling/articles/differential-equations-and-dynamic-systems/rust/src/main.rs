fn exponential_rate(x: f64, r: f64) -> f64 { r*x }
fn logistic_rate(x: f64, r: f64, k: f64) -> f64 { r*x*(1.0 - x/k) }

fn simulate(scenario: &str, logistic: bool) {
    let mut x = 10.0;
    let r = 0.35;
    let k = 100.0;
    let dt = 0.1;
    for n in 0..=100 {
        let t = n as f64 * dt;
        let rate = if logistic { logistic_rate(x,r,k) } else { exponential_rate(x,r) };
        println!("{},{},{:.6},{:.6},{:.6},{:.6},{:.6},explicit_euler,{}",
            scenario,
            if logistic {"dx_dt_equals_r_x_one_minus_x_over_K"} else {"dx_dt_equals_r_x"},
            t, x, rate, r, if logistic {k} else {-1.0},
            if logistic {"Logistic growth assumes a fixed carrying capacity."} else {"Exponential growth assumes no capacity constraint."});
        x += dt*rate;
    }
}

fn main() {
    println!("scenario,model_type,time,state,rate,growth_rate,carrying_capacity,method,warning");
    simulate("exponential_growth", false);
    simulate("logistic_growth", true);
}
