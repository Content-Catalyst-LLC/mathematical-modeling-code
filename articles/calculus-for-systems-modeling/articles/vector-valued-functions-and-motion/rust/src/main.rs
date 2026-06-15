const PI: f64 = std::f64::consts::PI;

fn position(t: f64) -> (f64, f64) { (t, t.sin()) }
fn distance_between(p: (f64, f64), q: (f64, f64)) -> f64 {
    ((q.0 - p.0).powi(2) + (q.1 - p.1).powi(2)).sqrt()
}

fn audit(step: f64, scenario: &str) {
    let count = ((2.0 * PI) / step) as usize + 1;
    let first = position(0.0);
    let mut prev = first;
    let mut arc = 0.0;
    let mut speed_sum = 0.0;
    let mut speed_max = 0.0;
    for i in 1..count {
        let p = position(i as f64 * step);
        let seg = distance_between(prev, p);
        let speed = seg / step;
        arc += seg;
        speed_sum += speed;
        if speed > speed_max { speed_max = speed; }
        prev = p;
    }
    let disp = distance_between(first, prev);
    let eff = disp / arc.max(1e-12);
    let warning = if step > 0.5 { "Time step is coarse; turns and speed variation may be undersampled." } else { "Synthetic trajectory audit; document units parameter meaning and sampling." };
    println!("{},{:.12},{},{:.12},{:.12},{:.12},{:.12},{:.12},trajectory r(t)=<t,sin(t)>,{}", scenario, step, count, arc, disp, eff, speed_sum/((count-1) as f64), speed_max, warning);
}

fn main() {
    println!("scenario,time_step,point_count,approximate_arc_length,displacement_magnitude,path_efficiency,average_speed,maximum_speed,domain_description,warning");
    audit(1.0, "coarse_time_step");
    audit(0.5, "medium_time_step");
    audit(0.25, "fine_time_step");
}
