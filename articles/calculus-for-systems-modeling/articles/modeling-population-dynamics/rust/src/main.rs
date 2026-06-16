fn exponential(n0:f64,r:f64,t:f64)->f64{ n0*(r*t).exp() }
fn logistic(n0:f64,r:f64,k:f64,t:f64)->f64{ k/(1.0+((k-n0)/n0)*(-r*t).exp()) }
fn main(){ let (n0,r,k)=(100.0,0.08,1000.0); println!("time,exponential,logistic"); for t in (0..=40).step_by(5){ let tf=t as f64; println!("{},{:.6},{:.6}",t,exponential(n0,r,tf),logistic(n0,r,k,tf)); } }
