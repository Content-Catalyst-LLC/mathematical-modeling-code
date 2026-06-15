fn tail_function(x:f64)->f64{(-0.4*x).exp()}

fn trap(func: fn(f64)->f64, a:f64, b:f64, n:usize)->f64{
    let dx = (b-a)/(n as f64);
    let mut total = 0.0;
    for i in 0..n {
        let x0 = a + dx*(i as f64);
        let x1 = x0 + dx;
        total += 0.5*(func(x0)+func(x1))*dx;
    }
    total
}

fn main(){
    let cutoffs = [2.0,4.0,8.0,12.0,20.0];
    let reference = 1.0/0.4;
    println!("cutoff,truncated_value,reference_value,tail_error");
    for cutoff in cutoffs {
        let truncated = trap(tail_function,0.0,cutoff,4000);
        let tail_error = reference - truncated;
        println!("{:.6},{:.12},{:.12},{:.12}",cutoff,truncated,reference,tail_error);
    }
}
