fn f(x: f64, y: f64) -> f64 { 3.0*x + 2.0*y + 0.5*x*y }
fn gx(_x: f64, y: f64) -> f64 { 3.0 + 0.5*y }
fn gy(x: f64, _y: f64) -> f64 { 2.0 + 0.5*x }
fn normalize(vx: f64, vy: f64) -> (f64, f64) {
    let norm = (vx*vx + vy*vy).sqrt();
    if norm == 0.0 { panic!("Direction vector must be nonzero."); }
    (vx / norm, vy / norm)
}
fn directional_derivative(x: f64, y: f64, ux: f64, uy: f64) -> f64 { gx(x,y)*ux + gy(x,y)*uy }
fn feasible_direction(x: f64, y: f64, ux: f64, uy: f64, step: f64) -> bool { x >= 0.0 && y >= 0.0 && x+y <= 10.0 && x+step*ux >= 0.0 && y+step*uy >= 0.0 && x+step*ux+y+step*uy <= 10.0 }

fn main() {
    let cases = vec![(4.0_f64,3.0_f64,1.0_f64,1.0_f64,0.25_f64),(4.0_f64,3.0_f64,2.0_f64,-1.0_f64,0.25_f64),(8.0_f64,1.0_f64,1.0_f64,1.0_f64,1.0_f64)];
    println!("x,y,direction_x,direction_y,unit_x,unit_y,gradient_x,gradient_y,directional_derivative,step_size,estimated_change,actual_change,absolute_error,feasible_direction,warning");
    for (x,y,vx,vy,step) in cases {
        let (ux, uy) = normalize(vx, vy);
        let deriv = directional_derivative(x,y,ux,uy);
        let estimated = step * deriv;
        let actual = f(x+step*ux,y+step*uy) - f(x,y);
        let feasible = feasible_direction(x,y,ux,uy,step);
        let warning = if feasible { "" } else { "Direction and step move outside the feasible region." };
        println!("{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{},{}", x,y,vx,vy,ux,uy,gx(x,y),gy(x,y),deriv,step,estimated,actual,(actual-estimated).abs(),feasible,warning);
    }
}
