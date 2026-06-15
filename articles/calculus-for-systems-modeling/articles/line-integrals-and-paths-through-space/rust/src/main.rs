const PI: f64 = std::f64::consts::PI;

fn path_point(t: f64) -> (f64, f64) { (t, t.sin()) }
fn scalar_field(_x: f64, y: f64) -> f64 { 1.0 + y*y }
fn vector_field(x: f64, _y: f64) -> (f64, f64) { (1.0, x) }
fn distance(p: (f64, f64), q: (f64, f64)) -> f64 { ((q.0-p.0).powi(2) + (q.1-p.1).powi(2)).sqrt() }
fn dot(a: (f64, f64), b: (f64, f64)) -> f64 { a.0*b.0 + a.1*b.1 }

fn audit(step: f64, scenario: &str) {
    let count = ((2.0*PI)/step) as usize + 1;
    let mut path_len = 0.0;
    let mut scalar_total = 0.0;
    let mut vector_total = 0.0;
    let mut align_sum = 0.0;
    let mut max_seg = 0.0;
    for i in 0..(count-1) {
        let p = path_point(i as f64 * step);
        let q = path_point((i+1) as f64 * step);
        let disp = (q.0-p.0, q.1-p.1);
        let seg = distance(p,q);
        let term = dot(vector_field(p.0,p.1), disp);
        path_len += seg;
        scalar_total += scalar_field(p.0,p.1) * seg;
        vector_total += term;
        align_sum += term / seg.max(1e-12);
        if seg > max_seg { max_seg = seg; }
    }
    let warning = if step > 0.5 { "Time step is coarse; path turns and field variation may be undersampled." } else { "Synthetic line-integral audit; document path field units and interpolation." };
    println!("{},{:.12},{},{:.12},{:.12},{:.12},{:.12},{:.12},path r(t)=<t,sin(t)>,{}", scenario, step, count, path_len, scalar_total, vector_total, align_sum/((count-1) as f64), max_seg, warning);
}

fn main() {
    println!("scenario,time_step,point_count,path_length,scalar_line_integral,vector_line_integral,average_alignment,maximum_segment_length,path_description,warning");
    audit(1.0, "coarse_path");
    audit(0.5, "medium_path");
    audit(0.25, "fine_path");
}
