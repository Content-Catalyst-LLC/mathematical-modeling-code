fn net_rate(t:f64)->f64{4.0*(t/2.0).sin()+1.0}
fn main(){
    let times = [0.0,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0];
    let mut signed_accumulation = 0.0;
    let mut absolute_accumulation = 0.0;
    for i in 0..times.len()-1 {
        let dt = times[i+1] - times[i];
        let r0 = net_rate(times[i]);
        let r1 = net_rate(times[i+1]);
        signed_accumulation += 0.5*(r0+r1)*dt;
        absolute_accumulation += 0.5*(r0.abs()+r1.abs())*dt;
    }
    println!("interval_start,interval_end,method,signed_accumulation,absolute_accumulation");
    println!("{:.6},{:.6},trapezoidal approximation,{:.12},{:.12}",times[0],times[times.len()-1],signed_accumulation,absolute_accumulation);
}
