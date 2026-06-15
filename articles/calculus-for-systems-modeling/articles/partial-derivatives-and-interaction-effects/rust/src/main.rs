fn system_response(x: f64, y: f64) -> f64 { 3.0*x + 2.0*y + 0.5*x*y }
fn partial_x(_x: f64, y: f64) -> f64 { 3.0 + 0.5*y }
fn partial_y(x: f64, _y: f64) -> f64 { 2.0 + 0.5*x }
fn cross_partial_xy(_x: f64, _y: f64) -> f64 { 0.5 }
fn is_feasible(x: f64, y: f64) -> bool { x >= 0.0 && y >= 0.0 && x + y <= 10.0 }

fn main() {
    let cases = vec![(2.0_f64,4.0_f64),(8.0_f64,4.0_f64),(6.0_f64,3.0_f64)];
    println!("x,y,output,partial_x,partial_y,cross_partial_xy,feasible,warning");
    for (x,y) in cases {
        let feasible = is_feasible(x,y);
        let warning = if feasible { "" } else { "Input combination is outside the feasible region." };
        println!("{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{},{}", x, y, system_response(x,y), partial_x(x,y), partial_y(x,y), cross_partial_xy(x,y), feasible, warning);
    }
}
