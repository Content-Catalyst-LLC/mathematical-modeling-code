fn f(x: f64, y: f64) -> f64 { 3.0*x + 2.0*y + 0.5*x*y }
fn fx(_x: f64, y: f64) -> f64 { 3.0 + 0.5*y }
fn fy(x: f64, _y: f64) -> f64 { 2.0 + 0.5*x }
fn total_differential(x: f64, y: f64, dx: f64, dy: f64) -> f64 { fx(x,y)*dx + fy(x,y)*dy }
fn feasible_displacement(x: f64, y: f64, dx: f64, dy: f64) -> bool { x >= 0.0 && y >= 0.0 && x + y <= 10.0 && x + dx >= 0.0 && y + dy >= 0.0 && x + dx + y + dy <= 10.0 }

fn main() {
    let cases = vec![(4.0_f64,3.0_f64,0.2_f64,-0.1_f64),(4.0_f64,3.0_f64,1.0_f64,1.0_f64),(8.0_f64,1.0_f64,1.0_f64,1.0_f64)];
    println!("x,y,dx,dy,baseline_output,actual_output,actual_change,differential_estimate,absolute_error,feasible_displacement,warning");
    for (x,y,dx,dy) in cases {
        let baseline = f(x,y);
        let actual = f(x+dx,y+dy);
        let change = actual - baseline;
        let estimate = total_differential(x,y,dx,dy);
        let feasible = feasible_displacement(x,y,dx,dy);
        let warning = if feasible { "" } else { "Displacement is outside the feasible region." };
        println!("{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{},{}", x, y, dx, dy, baseline, actual, change, estimate, (change-estimate).abs(), feasible, warning);
    }
}
