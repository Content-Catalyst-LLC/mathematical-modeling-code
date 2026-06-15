fn rates(x: f64, y: f64, alpha: f64, beta: f64, delta: f64, gamma: f64) -> (f64, f64) {
    (alpha*x - beta*x*y, delta*x*y - gamma*y)
}

fn main() {
    let alpha = 0.7;
    let beta = 0.05;
    let delta = 0.02;
    let gamma = 0.5;
    println!("x,y,dxdt,dydt,x_nullcline_residual,y_nullcline_residual,speed,warning");
    for xi in (0..=60).step_by(5) {
        for yi in (0..=30).step_by(3) {
            let x = xi as f64;
            let y = yi as f64;
            let (dxdt, dydt) = rates(x, y, alpha, beta, delta, gamma);
            let speed = (dxdt*dxdt + dydt*dydt).sqrt();
            println!("{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},{:.6},Vector-field values depend on parameter values state ranges and the assumed interaction structure.", x, y, dxdt, dydt, dxdt, dydt, speed);
        }
    }
}
