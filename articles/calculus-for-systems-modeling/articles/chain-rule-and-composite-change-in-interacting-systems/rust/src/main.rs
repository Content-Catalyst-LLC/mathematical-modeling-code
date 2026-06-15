fn emissions(t:f64)->f64{50.0*(0.015*t).exp()}
fn emissions_rate(t:f64)->f64{0.015*emissions(t)}
fn concentration(e:f64)->f64{0.5*e}
fn forcing(c:f64)->f64{(1.0+c).ln()}
fn main(){
  println!("t,emissions,concentration,forcing,temperature,emissions_rate,d_concentration_d_emissions,d_forcing_d_concentration,d_temperature_d_forcing,total_derivative");
  for t in [0.0,5.0,10.0,20.0,40.0] {
    let e=emissions(t); let c=concentration(e); let f=forcing(c); let temp=1.2*f;
    let s1=emissions_rate(t); let s2=0.5; let s3=1.0/(1.0+c); let s4=1.2; let total=s4*s3*s2*s1;
    println!("{:.6},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12}",t,e,c,f,temp,s1,s2,s3,s4,total);
  }
}
