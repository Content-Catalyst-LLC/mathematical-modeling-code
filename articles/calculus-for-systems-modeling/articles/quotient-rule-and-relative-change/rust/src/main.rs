fn resource(t:f64)->f64{1000.0*(-0.01*t).exp()}
fn resource_rate(t:f64)->f64{-0.01*resource(t)}
fn population(t:f64)->f64{100.0*(0.02*t).exp()}
fn population_rate(t:f64)->f64{0.02*population(t)}
fn main(){
  println!("t,numerator,denominator,ratio,numerator_rate,denominator_rate,numerator_effect,denominator_effect,quotient_derivative,ratio_relative_rate");
  for t in [0.0,5.0,10.0,20.0,40.0] {
    let f=resource(t); let g=population(t); let fp=resource_rate(t); let gp=population_rate(t);
    let ratio=f/g; let ne=fp/g; let de=-(f*gp)/(g*g); let qd=ne+de;
    println!("{:.6},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12}",t,f,g,ratio,fp,gp,ne,de,qd,qd/ratio);
  }
}
