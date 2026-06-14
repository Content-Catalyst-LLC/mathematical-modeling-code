fn linear_model(x: f64) -> f64 {
    10.0 + 2.0 * x
}

fn exponential_model(x: f64) -> f64 {
    10.0 * (0.18 * x).exp()
}

fn logistic_model(x: f64) -> f64 {
    100.0 / (1.0 + (-0.75 * (x - 5.0)).exp())
}

fn threshold_model(x: f64) -> f64 {
    if x < 5.0 { 20.0 } else { 80.0 }
}

fn main() {
    let x = 10.0;
    println!("model,final_value");
    println!("linear_growth,{:.6}", linear_model(x));
    println!("exponential_growth,{:.6}", exponential_model(x));
    println!("logistic_growth,{:.6}", logistic_model(x));
    println!("threshold_response,{:.6}", threshold_model(x));
}
