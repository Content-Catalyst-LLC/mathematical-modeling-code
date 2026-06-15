fn population(t:f64)->f64{100.0*(0.01*t).exp()}
fn population_rate(t:f64)->f64{0.01*population(t)}
fn affluence(t:f64)->f64{2.0*(0.02*t).exp()}
fn affluence_rate(t:f64)->f64{0.02*affluence(t)}
fn main(){
  println!("rule,model_structure,t,derivative_value,component_a,component_b,warning");
  for t in [0.0,5.0,10.0,20.0] {
    let a=population_rate(t)*affluence(t);
    let b=population(t)*affluence_rate(t);
    println!("product_rule,impact = population * affluence,{:.6},{:.12},{:.12},{:.12},",t,a+b,a,b);
  }
}
