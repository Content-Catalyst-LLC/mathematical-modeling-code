use std::f64::consts::PI;

fn vector_field(x: f64, y: f64) -> (f64, f64) { (-y, x) }
fn dot(a: (f64, f64), b: (f64, f64)) -> f64 { a.0*b.0 + a.1*b.1 }

fn audit(radius: f64, segments: usize, scenario: &str) {
    let mut flux_total = 0.0;
    let mut circulation_total = 0.0;
    let mut tangent_sum = 0.0;
    let mut normal_sum = 0.0;

    for i in 0..segments {
        let theta0 = 2.0*PI*i as f64/segments as f64;
        let theta1 = 2.0*PI*(i+1) as f64/segments as f64;
        let (x0,y0) = (radius*theta0.cos(), radius*theta0.sin());
        let (x1,y1) = (radius*theta1.cos(), radius*theta1.sin());
        let (xm,ym) = (0.5*(x0+x1), 0.5*(y0+y1));
        let (dx,dy) = (x1-x0, y1-y0);
        let segment_length = (dx*dx + dy*dy).sqrt();
        let tangent = (dx/segment_length, dy/segment_length);
        let normal = (xm/radius, ym/radius);
        let field = vector_field(xm, ym);
        circulation_total += dot(field, (dx,dy));
        flux_total += dot(field, normal) * segment_length;
        tangent_sum += dot(field, tangent);
        normal_sum += dot(field, normal);
    }

    let warning = if segments < 32 { "Coarse path sampling; circulation and flux should be checked with more segments." } else { "Synthetic flow audit; document field meaning orientation units and boundary choice." };
    println!("{},{},{:.12},{:.12},{:.12},{:.12},rotating field F=<-y,x>,counterclockwise circle with radius 1,{}", scenario, segments, flux_total, circulation_total, tangent_sum/(segments as f64), normal_sum/(segments as f64), warning);
}

fn main() {
    println!("scenario,segment_count,approximate_flux,approximate_circulation,mean_tangential_alignment,mean_normal_alignment,field_description,geometry_description,warning");
    audit(1.0, 16, "coarse_circle");
    audit(1.0, 64, "medium_circle");
    audit(1.0, 256, "fine_circle");
}
