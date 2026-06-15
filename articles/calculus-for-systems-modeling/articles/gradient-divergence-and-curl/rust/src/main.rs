fn gradient(x: f64, y: f64) -> (f64, f64) { (2.0*x, 2.0*y) }
fn divergence(_x: f64, _y: f64) -> f64 { 0.0 }
fn curl_2d(_x: f64, _y: f64) -> f64 { 2.0 }

fn audit(step: f64, scenario: &str) {
    let n = (2.0 / step) as usize + 1;
    let mut count = 0usize;
    let mut grad_sum = 0.0;
    let mut max_grad = 0.0;
    let mut div_sum = 0.0;
    let mut curl_sum = 0.0;
    let mut max_abs_curl = 0.0;

    for i in 0..n {
        let x = -1.0 + i as f64 * step;
        for j in 0..n {
            let y = -1.0 + j as f64 * step;
            let (gx, gy) = gradient(x,y);
            let gmag = (gx*gx + gy*gy).sqrt();
            let div = divergence(x,y);
            let curl = curl_2d(x,y);
            count += 1;
            grad_sum += gmag;
            if gmag > max_grad { max_grad = gmag; }
            div_sum += div;
            curl_sum += curl;
            if curl.abs() > max_abs_curl { max_abs_curl = curl.abs(); }
        }
    }

    let warning = if step > 0.5 { "Grid step is coarse; local derivative structure may be undersampled." } else { "Synthetic field-operator audit; document field definitions units grid and boundary rules." };
    println!("{},{:.12},{},{:.12},{:.12},{:.12},{:.12},{:.12},scalar f=x^2+y^2; vector F=<-y,x>,{}", scenario, step, count, grad_sum/(count as f64), max_grad, div_sum/(count as f64), curl_sum/(count as f64), max_abs_curl, warning);
}

fn main() {
    println!("scenario,grid_step,point_count,mean_gradient_magnitude,maximum_gradient_magnitude,mean_divergence,mean_curl,maximum_abs_curl,field_description,warning");
    audit(1.0, "coarse_grid");
    audit(0.5, "medium_grid");
    audit(0.25, "fine_grid");
}
