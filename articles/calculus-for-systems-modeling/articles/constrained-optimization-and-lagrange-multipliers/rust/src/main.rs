fn objective(x: f64, y: f64) -> f64 { x*x + 2.0*y*y }

fn main() {
    let targets = vec![12.0_f64, 18.0_f64, 24.0_f64];
    println!("x,y,objective_value,constraint_value,constraint_target,constraint_residual,lambda_value,gradient_f_x,gradient_f_y,gradient_g_x,gradient_g_y,stationarity_residual_norm,feasible,warning");
    for target in targets {
        let y = target / 3.0;
        let x = 2.0 * target / 3.0;
        let lambda = 2.0 * x;
        let gfx = 2.0*x;
        let gfy = 4.0*y;
        let ggx = 1.0;
        let ggy = 1.0;
        let sx = gfx - lambda*ggx;
        let sy = gfy - lambda*ggy;
        let norm = (sx*sx + sy*sy).sqrt();
        let cval = x + y;
        let cres = cval - target;
        let feasible = cres.abs() <= 1e-9;
        let warning = if feasible && norm <= 1e-8 { "Multiplier interpretation is local and unit-dependent." } else { "Review feasibility or stationarity." };
        println!("{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{:.12},{},{}", x,y,objective(x,y),cval,target,cres,lambda,gfx,gfy,ggx,ggy,norm,feasible,warning);
    }
}
