fn mean(values: &[f64]) -> f64 {
    values.iter().sum::<f64>() / values.len() as f64
}

fn sample_variance(values: &[f64]) -> f64 {
    let m = mean(values);
    values.iter().map(|x| (x - m).powi(2)).sum::<f64>() / (values.len() as f64 - 1.0)
}

fn main() {
    let values = vec![18.4, 36.7, 62.1, 28.9, 64.8, 13.7, 43.5, 29.8, 79.4, 30.2];
    let m = mean(&values);
    let variance = sample_variance(&values);
    let sd = variance.sqrt();

    println!("Mean: {:.6}", m);
    println!("Sample variance: {:.6}", variance);
    println!("Sample standard deviation: {:.6}", sd);
}
