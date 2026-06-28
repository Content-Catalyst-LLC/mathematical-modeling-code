fn main() {
    let a = 3.0;
    let b = 1.0;
    let c = 2.0;
    let d = 4.0;
    let y1 = 7.0;
    let y2 = 8.0;

    let det = a * d - b * c;

    if det == 0.0 {
        println!("Matrix is singular; recovery is not unique.");
        return;
    }

    let x1 = (d * y1 - b * y2) / det;
    let x2 = (-c * y1 + a * y2) / det;

    println!("Recovered state: x1 = {:.2}, x2 = {:.2}", x1, x2);
}
