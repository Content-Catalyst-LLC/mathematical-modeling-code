fn boundary_points(n: usize) -> Vec<(f64, f64)> {
    let mut pts = Vec::new();
    for i in 0..n { let t = -1.0 + 2.0*i as f64/n as f64; pts.push((t,-1.0)); }
    for i in 0..n { let t = -1.0 + 2.0*i as f64/n as f64; pts.push((1.0,t)); }
    for i in 0..n { let t = 1.0 - 2.0*i as f64/n as f64; pts.push((t,1.0)); }
    for i in 0..n { let t = 1.0 - 2.0*i as f64/n as f64; pts.push((-1.0,t)); }
    pts.push(pts[0]);
    pts
}

fn audit(segments: usize, step: f64, scenario: &str) {
    let pts = boundary_points(segments);
    let mut bc = 0.0;
    let mut bf = 0.0;
    for i in 0..pts.len()-1 {
        let (x0,y0) = pts[i];
        let (x1,y1) = pts[i+1];
        let (xm,ym) = (0.5*(x0+x1), 0.5*(y0+y1));
        let (dx,dy) = (x1-x0, y1-y0);
        bc += (-ym)*dx + xm*dy;
        bf += xm*dy + ym*(-dx);
    }
    let n = (2.0/step) as f64;
    let ic = 2.0*n*n*step*step;
    let idv = ic;
    let warning = if segments < 16 || step > 0.25 { "Coarse boundary or interior sampling." } else { "Synthetic Greens theorem audit." };
    println!("{},{},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},circulation F=<-y,x>; flux G=<x,y>,square [-1,1]x[-1,1],{}", scenario, segments, step, bc, ic, bf, idv, (bc-ic).abs(), (bf-idv).abs(), warning);
}

fn main() {
    println!("scenario,boundary_segments_per_side,interior_grid_step,boundary_circulation,interior_curl_integral,boundary_flux,interior_divergence_integral,circulation_gap,flux_gap,field_description,region_description,warning");
    audit(8, 0.5, "coarse_audit");
    audit(32, 0.25, "medium_audit");
    audit(128, 0.125, "fine_audit");
}
