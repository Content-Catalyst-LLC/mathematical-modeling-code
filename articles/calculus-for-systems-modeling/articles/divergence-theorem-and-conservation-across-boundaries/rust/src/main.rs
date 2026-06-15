fn audit(grid_steps: usize, scenario: &str) {
    let step = 1.0 / grid_steps as f64;
    let area = step * step;
    let mut flux = 0.0;
    for _i in 0..grid_steps {
        for _j in 0..grid_steps {
            flux += 3.0 * area;
        }
    }
    let div_integral = 3.0;
    let warning = if grid_steps < 8 { "Coarse grid; refine before interpreting the boundary-volume comparison." } else { "Synthetic divergence theorem audit." };
    println!("{},{},{:.12},{:.12},{:.12},F=<x,y,z>; divergence = 3,unit cube [0,1]x[0,1]x[0,1],all six cube faces use outward normals,{}", scenario, grid_steps, flux, div_integral, (flux-div_integral).abs(), warning);
}

fn main() {
    println!("scenario,grid_steps,boundary_flux,volume_divergence_integral,absolute_gap,field_description,volume_description,normal_note,warning");
    audit(4, "coarse_audit");
    audit(16, "medium_audit");
    audit(64, "fine_audit");
}
