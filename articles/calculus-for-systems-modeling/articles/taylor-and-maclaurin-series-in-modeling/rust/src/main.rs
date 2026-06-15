fn factorial(n: u32) -> f64 {
    (1..=n).fold(1.0, |acc, v| acc * v as f64)
}

fn taylor_exp(x: f64, order: u32) -> f64 {
    (0..=order).map(|n| x.powi(n as i32) / factorial(n)).sum()
}

fn main() {
    let cases = vec![(0.5_f64, 2_u32), (1.0_f64, 10_u32), (3.0_f64, 10_u32)];
    println!("function_name,center,x_value,order,approximation,reference_value,absolute_error,warning");

    for (x, order) in cases {
        let approximation = taylor_exp(x, order);
        let reference = x.exp();
        let warning = if x.abs() <= 2.0 { "" } else { "Evaluation is far from the Maclaurin center; review truncation error carefully." };
        println!("exp(x),0.0,{:.12},{},{:.12},{:.12},{:.12},{}", x, order, approximation, reference, (reference-approximation).abs(), warning);
    }
}
