fn rate(t:f64)->f64{2.0+t.sin()+0.1*t}
fn trueint(t:f64)->f64{2.0*t-t.cos()+1.0+0.05*t*t}
fn main(){let h=0.1_f64; let mut left=0.0; let mut trap=0.0; println!("index,time,rate,left_cumulative,trapezoid_cumulative,true_cumulative,error"); for i in 0..=100{let t=i as f64*h; let r=rate(t); if i>0{left+=rate((i-1) as f64*h)*h; trap+=0.5*(rate((i-1) as f64*h)+r)*h;} let truth=trueint(t)-trueint(0.0); println!("{},{:.6},{:.12},{:.12},{:.12},{:.12},{:.12}",i,t,r,left,trap,truth,(trap-truth).abs());}}
