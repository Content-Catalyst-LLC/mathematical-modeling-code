fn forward_model(x:f64)->f64{x.ln_1p()}
fn forward_derivative(x:f64)->f64{1.0/(1.0+x)}
fn inverse_model(y:f64)->f64{y.exp()-1.0}
fn main(){
  println!("target_output,recovered_input,forward_check,residual,forward_derivative,inverse_sensitivity,domain_valid");
  for y in [0.0,0.5,1.0,1.5,2.0] {
    let x=inverse_model(y);
    let ycheck=forward_model(x);
    let residual=ycheck-y;
    let derivative=forward_derivative(x);
    let invsens=1.0/derivative;
    let domain_valid=x > -1.0;
    println!("{:.6},{:.12},{:.12},{:.12},{:.12},{:.12},{}",y,x,ycheck,residual,derivative,invsens,domain_valid);
  }
}
