fn main() {
    let a = [
        [0.82, 0.10, 0.08],
        [0.12, 0.76, 0.12],
        [0.06, 0.18, 0.76],
    ];

    let x = [0.70, 0.20, 0.10];
    let mut y = [0.0; 3];

    for i in 0..3 {
        for j in 0..3 {
            y[i] += a[i][j] * x[j];
        }
    }

    println!("Transformed state: {:.6} {:.6} {:.6}", y[0], y[1], y[2]);
}
