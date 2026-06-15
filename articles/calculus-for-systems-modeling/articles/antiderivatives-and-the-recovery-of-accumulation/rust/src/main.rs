fn net_flow(t:f64)->f64{(12.0+0.5*t)-(7.0+0.2*t)}
fn main(){
    let times = [0.0,1.0,2.0,3.0,4.0,5.0,6.0];
    let mut stock = 100.0;
    println!("time,net_flow,recovered_stock,method");
    println!("{:.6},{:.12},{:.12},initial condition",times[0],net_flow(times[0]),stock);
    for i in 1..times.len(){
        let previous = times[i-1];
        let current = times[i];
        let dt = current - previous;
        stock += 0.5 * (net_flow(previous) + net_flow(current)) * dt;
        println!("{:.6},{:.12},{:.12},trapezoidal accumulation",current,net_flow(current),stock);
    }
}
