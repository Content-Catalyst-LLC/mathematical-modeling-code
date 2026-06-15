fn g(x:f64)->f64{x*x+1.0}
fn g_prime(x:f64)->f64{2.0*x}
fn f(u:f64)->f64{u.sqrt()}
fn integrand_x(x:f64)->f64{f(g(x))*g_prime(x)}

fn trap(func: fn(f64)->f64, a:f64, b:f64, n:usize)->f64{
    let step = (b-a)/(n as f64);
    let mut total = 0.0;
    for i in 0..n {
        let x0 = a + step*(i as f64);
        let x1 = x0 + step;
        total += 0.5*(func(x0)+func(x1))*step;
    }
    total
}

fn main(){
    let a = 1.0;
    let b = 3.0;
    let ua = g(a);
    let ub = g(b);
    let direct = trap(integrand_x,a,b,400);
    let transformed = trap(f,ua,ub,400);
    let residual = direct - transformed;
    println!("original_start,original_end,transformed_start,transformed_end,direct_integral,transformed_integral,residual");
    println!("{:.6},{:.6},{:.6},{:.6},{:.12},{:.12},{:.12}",a,b,ua,ub,direct,transformed,residual);
}
