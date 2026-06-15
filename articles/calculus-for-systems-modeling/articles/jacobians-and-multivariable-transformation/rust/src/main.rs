fn f_model(x: f64, y: f64) -> (f64, f64) { (x*x + y, x*y + 3.0*y) }

fn main() {
    let cases = vec![(2.0_f64,1.0_f64,0.1_f64,-0.05_f64),(2.0_f64,1.0_f64,0.5_f64,0.5_f64),(0.0_f64,0.0_f64,0.1_f64,0.1_f64)];
    println!("x,y,dx,dy,j11,j12,j21,j22,determinant,approximate_change_1,approximate_change_2,actual_change_1,actual_change_2,error_norm,warning");
    for (x,y,dx,dy) in cases {
        let j11 = 2.0*x; let j12 = 1.0; let j21 = y; let j22 = x + 3.0;
        let baseline = f_model(x,y);
        let actual = f_model(x+dx,y+dy);
        let ac1 = j11*dx + j12*dy;
        let ac2 = j21*dx + j22*dy;
        let rc1 = actual.0 - baseline.0;
        let rc2 = actual.1 - baseline.1;
        let det = j11*j22 - j12*j21;
        let err = ((rc1-ac1).powi(2) + (rc2-ac2).powi(2)).sqrt();
        let warning = if det.abs() > 1e-8 { "" } else { "Jacobian is singular or near singular." };
        println!("{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{}", x,y,dx,dy,j11,j12,j21,j22,det,ac1,ac2,rc1,rc2,err,warning);
    }
}
