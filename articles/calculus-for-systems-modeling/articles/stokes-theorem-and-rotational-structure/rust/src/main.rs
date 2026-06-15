use std::f64::consts::PI;

fn audit(radius: f64, segments: usize, radial_steps: usize, scenario: &str) {
    let mut circulation = 0.0;
    for i in 0..segments {
        let theta0 = 2.0*PI*i as f64/segments as f64;
        let theta1 = 2.0*PI*(i+1) as f64/segments as f64;
        let (x0,y0) = (radius*theta0.cos(), radius*theta0.sin());
        let (x1,y1) = (radius*theta1.cos(), radius*theta1.sin());
        let (xm,ym) = (0.5*(x0+x1), 0.5*(y0+y1));
        let (dx,dy) = (x1-x0, y1-y0);
        circulation += (-ym)*dx + xm*dy;
    }

    let mut curl_flux = 0.0;
    for i in 0..radial_steps {
        let r0 = radius*i as f64/radial_steps as f64;
        let r1 = radius*(i+1) as f64/radial_steps as f64;
        let ring_area = PI*(r1*r1 - r0*r0);
        curl_flux += 2.0*ring_area;
    }

    let warning = if segments < 64 || radial_steps < 16 { "Coarse boundary or surface sampling." } else { "Synthetic Stokes theorem audit." };
    println!("{},{:.12},{},{},{:.12},{:.12},{:.12},F=<-y,x,0>; curl F=<0,0,2>,horizontal disk with upward normal,counterclockwise boundary orientation viewed from positive z,{}", scenario, radius, segments, radial_steps, circulation, curl_flux, (circulation-curl_flux).abs(), warning);
}

fn main() {
    println!("scenario,radius,boundary_segments,radial_steps,boundary_circulation,surface_curl_flux,absolute_gap,field_description,surface_description,orientation_note,warning");
    audit(1.0, 32, 8, "coarse_audit");
    audit(1.0, 128, 32, "medium_audit");
    audit(1.0, 512, 128, "fine_audit");
}
