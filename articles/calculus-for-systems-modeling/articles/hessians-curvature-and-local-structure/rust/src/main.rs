fn f_model(x: f64, y: f64) -> f64 { x*x + x*y + 3.0*y*y + 0.2*x*x*y }
fn gradient(x: f64, y: f64) -> (f64, f64) { (2.0*x + y + 0.4*x*y, x + 6.0*y + 0.2*x*x) }
fn classify(h11: f64, h12: f64, h21: f64, h22: f64) -> &'static str {
    let det = h11*h22 - h12*h21;
    if det > 0.0 && h11 > 0.0 { "positive definite" }
    else if det > 0.0 && h11 < 0.0 { "negative definite" }
    else if det < 0.0 { "indefinite" }
    else { "semidefinite or inconclusive" }
}

fn main() {
    let cases = vec![(2.0_f64,1.0_f64,0.1_f64,-0.05_f64),(2.0_f64,1.0_f64,0.5_f64,0.5_f64),(-5.0_f64,0.0_f64,0.2_f64,0.1_f64)];
    println!("x,y,dx,dy,gradient_x,gradient_y,h11,h12,h21,h22,determinant,trace,classification,first_order_change,second_order_change,actual_change,first_order_error,second_order_error,warning");
    for (x,y,dx,dy) in cases {
        let (gx,gy) = gradient(x,y);
        let h11 = 2.0 + 0.4*y; let h12 = 1.0 + 0.4*x; let h21 = h12; let h22 = 6.0;
        let det = h11*h22 - h12*h21;
        let cl = classify(h11,h12,h21,h22);
        let first = gx*dx + gy*dy;
        let second = first + 0.5*(h11*dx*dx + 2.0*h12*dx*dy + h22*dy*dy);
        let actual = f_model(x+dx,y+dy) - f_model(x,y);
        let warning = if det < 0.0 { "Hessian is indefinite; local structure is saddle-like." } else if det.abs() < 1e-8 { "Hessian is singular or nearly singular." } else { "" };
        println!("{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{},{:.12},{:.12},{:.12},{:.12},{:.12},{}", x,y,dx,dy,gx,gy,h11,h12,h21,h22,det,h11+h22,cl,first,second,actual,(actual-first).abs(),(actual-second).abs(),warning);
    }
}
