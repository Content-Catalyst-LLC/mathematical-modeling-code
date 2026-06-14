fn piecewise_system(x: f64) -> f64 {
    if x < 5.0 {
        2.0 + 0.5 * x
    } else {
        6.0 + 1.4 * (x - 5.0)
    }
}

fn classify(level_jump: f64, slope_change: f64) -> &'static str {
    if level_jump > 1.0 && slope_change > 0.5 {
        "level_and_slope_break"
    } else if level_jump > 1.0 {
        "possible_jump"
    } else if slope_change > 0.5 {
        "possible_slope_break"
    } else {
        "ok"
    }
}

fn main() {
    let xs: Vec<f64> = (0..=40).map(|i| i as f64 * 0.25).collect();
    let ys: Vec<f64> = xs.iter().map(|x| piecewise_system(*x)).collect();

    println!("x,y,left_slope,right_slope,slope_change,level_jump,flag");

    for i in 0..xs.len() {
        if i == 0 || i == xs.len() - 1 {
            println!("{:.6},{:.6},,,,,ok", xs[i], ys[i]);
        } else {
            let left_slope = (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1]);
            let right_slope = (ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]);
            let slope_change = (right_slope - left_slope).abs();
            let level_jump = (ys[i] - ys[i - 1]).abs();
            println!("{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{}",
                xs[i], ys[i], left_slope, right_slope, slope_change, level_jump, classify(level_jump, slope_change));
        }
    }
}
