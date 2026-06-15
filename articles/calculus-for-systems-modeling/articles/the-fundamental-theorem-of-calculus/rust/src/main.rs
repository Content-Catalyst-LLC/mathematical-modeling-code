fn state_value(t:f64)->f64{50.0+2.0*t+3.0*t.sin()}
fn rate_value(t:f64)->f64{2.0+3.0*t.cos()}

fn main(){
    let times = [0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0];
    let mut accumulated_rate = 0.0;
    for i in 0..times.len()-1 {
        let dt = times[i+1] - times[i];
        accumulated_rate += 0.5 * (rate_value(times[i]) + rate_value(times[i+1])) * dt;
    }
    let endpoint_difference = state_value(times[times.len()-1]) - state_value(times[0]);
    let residual = endpoint_difference - accumulated_rate;
    println!("interval_start,interval_end,endpoint_difference,accumulated_rate,residual");
    println!("{:.6},{:.6},{:.12},{:.12},{:.12}",times[0],times[times.len()-1],endpoint_difference,accumulated_rate,residual);
}
