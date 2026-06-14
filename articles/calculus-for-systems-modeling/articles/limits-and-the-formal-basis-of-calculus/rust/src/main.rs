fn f(x: f64) -> f64 {
    (0.2 * x).exp()
}

fn exact_derivative(x: f64) -> f64 {
    0.2 * (0.2 * x).exp()
}

fn forward_difference(x: f64, h: f64) -> f64 {
    (f(x + h) - f(x)) / h
}

fn central_difference(x: f64, h: f64) -> f64 {
    (f(x + h) - f(x - h)) / (2.0 * h)
}

fn richardson(central_h: f64, central_h2: f64) -> f64 {
    (4.0 * central_h2 - central_h) / 3.0
}

fn main() {
    let x = 5.0;
    let exact = exact_derivative(x);
    let h_values = [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125];

    println!("method,x,h,estimate,exact,absolute_error");

    for h in h_values {
        let fd = forward_difference(x, h);
        let cd = central_difference(x, h);
        let cd2 = central_difference(x, h / 2.0);
        let rich = richardson(cd, cd2);

        println!("forward_difference,{:.6},{:.6},{:.12},{:.12},{:.12}", x, h, fd, exact, (fd - exact).abs());
        println!("central_difference,{:.6},{:.6},{:.12},{:.12},{:.12}", x, h, cd, exact, (cd - exact).abs());
        println!("richardson_central,{:.6},{:.6},{:.12},{:.12},{:.12}", x, h, rich, exact, (rich - exact).abs());
    }
}
