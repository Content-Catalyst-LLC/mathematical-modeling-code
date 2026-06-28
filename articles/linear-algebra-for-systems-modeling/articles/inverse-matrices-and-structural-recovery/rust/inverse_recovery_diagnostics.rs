fn main() {
    let a: f64 = 3.0;
    let b: f64 = 1.0;
    let c: f64 = 2.0;
    let d: f64 = 4.0;
    let y1: f64 = 7.0;
    let y2: f64 = 8.0;

    let det = a * d - b * c;
    println!("det(A) = {:.8}", det);

    if det.abs() < 1e-12 {
        println!("Matrix is singular or numerically near-singular.");
        return;
    }

    let x1 = (d * y1 - b * y2) / det;
    let x2 = (-c * y1 + a * y2) / det;

    let r1 = a * x1 + b * x2 - y1;
    let r2 = c * x1 + d * x2 - y2;
    let residual_norm = (r1 * r1 + r2 * r2).sqrt();

    println!("Recovered state: x1 = {:.8}, x2 = {:.8}", x1, x2);
    println!("Residual norm: {:.8e}", residual_norm);
}
