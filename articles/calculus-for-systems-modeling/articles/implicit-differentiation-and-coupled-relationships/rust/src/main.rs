fn equilibrium_state(p:f64)->f64{(-p + (p*p + 40.0).sqrt()) / 2.0}
fn constraint(x:f64,p:f64)->f64{x*x + p*x - 10.0}
fn partial_state(x:f64,p:f64)->f64{2.0*x + p}
fn partial_parameter(x:f64,_p:f64)->f64{x}
fn main(){
  println!("parameter,equilibrium_state,constraint_value,partial_state,partial_parameter,implicit_sensitivity");
  for p in [-3.0,-1.0,0.0,1.0,3.0] {
    let x=equilibrium_state(p);
    let gx=partial_state(x,p);
    let gp=partial_parameter(x,p);
    let sens=-gp/gx;
    println!("{:.6},{:.12},{:.12},{:.12},{:.12},{:.12}",p,x,constraint(x,p),gx,gp,sens);
  }
}
