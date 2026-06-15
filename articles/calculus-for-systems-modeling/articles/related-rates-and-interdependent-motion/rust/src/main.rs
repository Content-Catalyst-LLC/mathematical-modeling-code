fn volume(h:f64)->f64{12.0*h*h}
fn d_volume_d_height(h:f64)->f64{24.0*h}
fn height_path(t:f64)->f64{2.0 + 0.08*t}
fn height_rate(_t:f64)->f64{0.08}
fn main(){
  println!("time,height,height_rate,volume,structural_derivative,inferred_volume_rate");
  for t in [0.0,5.0,10.0,20.0,40.0] {
    let h=height_path(t);
    let hr=height_rate(t);
    let v=volume(h);
    let structural=d_volume_d_height(h);
    let inferred=structural*hr;
    println!("{:.6},{:.12},{:.12},{:.12},{:.12},{:.12}",t,h,hr,v,structural,inferred);
  }
}
