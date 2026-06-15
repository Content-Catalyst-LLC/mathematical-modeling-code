fn system_response(x: f64, y: f64) -> f64 { 3.0*x + 2.0*y + 0.5*x*y }
fn is_feasible(x: f64, y: f64) -> bool { x >= 0.0 && y >= 0.0 && x + y <= 10.0 }
fn main() {
    let cases = vec![(2.0_f64,4.0_f64),(8.0_f64,4.0_f64),(6.0_f64,3.0_f64)];
    println!("x,y,output,feasible,warning");
    for (x,y) in cases {
        let feasible = is_feasible(x,y);
        let warning = if feasible { "" } else { "Input combination is outside the feasible region." };
        println!("{:.12},{:.12},{:.12},{},{}", x, y, system_response(x,y), feasible, warning);
    }
}
