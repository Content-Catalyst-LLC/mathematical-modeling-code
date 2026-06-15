fn response_function(x:f64)->f64{10.0*(x+1.0).sqrt()}
fn analytic_derivative(x:f64)->f64{5.0/(x+1.0).sqrt()}
fn elasticity(x:f64)->Option<f64>{
    let y=response_function(x);
    if x==0.0 || y==0.0 {None} else {Some((x/y)*analytic_derivative(x))}
}
fn main(){
  println!("x,value,derivative,elasticity");
  for x in [0.0,0.5,1.0,4.0,9.0,24.0] {
    let e = elasticity(x).map(|v| v.to_string()).unwrap_or_else(|| "NA".to_string());
    println!("{:.6},{:.12},{:.12},{}",x,response_function(x),analytic_derivative(x),e);
  }
}
