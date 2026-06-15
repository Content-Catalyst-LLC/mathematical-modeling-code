fn logistic(x:f64)->f64{1.0/(1.0+(-x).exp())}
fn first_derivative(x:f64)->f64{let y=logistic(x); y*(1.0-y)}
fn second_derivative(x:f64)->f64{let y=logistic(x); y*(1.0-y)*(1.0-2.0*y)}
fn curvature(x:f64)->f64{let fp=first_derivative(x); let fpp=second_derivative(x); fpp.abs()/((1.0+fp*fp).powf(1.5))}
fn main(){
  println!("x,value,first_derivative,second_derivative,curvature");
  for x in [-4.0,-2.0,-1.0,0.0,1.0,2.0,4.0] {
    println!("{:.6},{:.12},{:.12},{:.12},{:.12}",x,logistic(x),first_derivative(x),second_derivative(x),curvature(x));
  }
}
