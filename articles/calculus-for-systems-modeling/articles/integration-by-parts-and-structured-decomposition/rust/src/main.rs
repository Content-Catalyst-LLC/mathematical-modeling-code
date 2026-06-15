fn u(x:f64)->f64{1.0+x}
fn u_prime(_x:f64)->f64{1.0}
fn v(x:f64)->f64{(-0.3*x).exp()*x.sin()}
fn v_prime(x:f64)->f64{(-0.3*x).exp()*(x.cos()-0.3*x.sin())}
fn direct_integrand(x:f64)->f64{u(x)*v_prime(x)}
fn residual_integrand(x:f64)->f64{v(x)*u_prime(x)}

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
    let a = 0.0;
    let b = 4.0;
    let direct = trap(direct_integrand,a,b,800);
    let residual = trap(residual_integrand,a,b,800);
    let boundary = u(b)*v(b)-u(a)*v(a);
    let decomposed = boundary - residual;
    let decomp_resid = direct - decomposed;
    println!("interval_start,interval_end,direct_integral,boundary_term,residual_integral,decomposed_value,decomposition_residual");
    println!("{:.6},{:.6},{:.12},{:.12},{:.12},{:.12},{:.12}",a,b,direct,boundary,residual,decomposed,decomp_resid);
}
