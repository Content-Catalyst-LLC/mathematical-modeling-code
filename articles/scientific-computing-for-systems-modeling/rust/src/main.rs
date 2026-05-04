fn trapezoid_integral(start: f64, end: f64, intervals: usize) -> f64 {
    let width = (end - start) / intervals as f64;
    let mut total = 0.0;

    for i in 1..=intervals {
        let x0 = start + (i as f64 - 1.0) * width;
        let x1 = start + i as f64 * width;
        let y0 = x0.sin() + 1.5;
        let y1 = x1.sin() + 1.5;
        total += 0.5 * (y0 + y1) * width;
    }

    total
}

fn main() {
    let estimate = trapezoid_integral(0.0, 10.0, 500);
    println!("Trapezoid integral estimate: {:.8}", estimate);
}
