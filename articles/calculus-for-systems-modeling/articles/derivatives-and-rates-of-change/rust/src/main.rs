fn response(x:f64)->f64{(0.2*x).exp()}
fn exact(x:f64)->f64{0.2*(0.2*x).exp()}
fn avg(a:f64,b:f64)->f64{(response(b)-response(a))/(b-a)}
fn fwd(x:f64,h:f64)->f64{(response(x+h)-response(x))/h}
fn bwd(x:f64,h:f64)->f64{(response(x)-response(x-h))/h}
fn cen(x:f64,h:f64)->f64{(response(x+h)-response(x-h))/(2.0*h)}
fn elast(d:f64,x:f64)->f64{(x/response(x))*d}
fn main(){
  let x=5.0; let exact=exact(x); let hs=[1.0,0.5,0.25,0.125,0.0625];
  println!("method,x0,h,estimate,exact,absolute_error,elasticity");
  for h in hs {
    let rows=[("average_rate_right",avg(x,x+h)),("forward_difference",fwd(x,h)),("backward_difference",bwd(x,h)),("central_difference",cen(x,h))];
    for (m,e) in rows { println!("{},{:.6},{:.6},{:.12},{:.12},{:.12},{:.12}",m,x,h,e,exact,(e-exact).abs(),elast(e,x)); }
  }
}
