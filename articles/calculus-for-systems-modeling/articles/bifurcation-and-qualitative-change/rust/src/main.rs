fn classify(d: f64) -> &'static str {
    if d < -1e-8 { "locally_stable" }
    else if d > 1e-8 { "locally_unstable" }
    else { "inconclusive_at_critical_value" }
}

fn main() {
    println!("model,parameter_mu,equilibrium,derivative_value,stability,branch_status,warning");
    for step in -20..=40 {
        let mu = step as f64 / 10.0;
        if mu < 0.0 {
            println!("saddle_node_normal_form,{:.6},,,no_real_equilibrium,equilibrium_absent,For mu below zero the saddle-node normal form has no real equilibrium.", mu);
        } else if mu.abs() < 1e-12 {
            let eq = 0.0;
            let d = -2.0 * eq;
            println!("saddle_node_normal_form,{:.6},{:.6},{:.6},{},critical_branch,Bifurcation interpretation depends on model form parameter meaning and domain validity.", mu, eq, d, classify(d));
        } else {
            let root = mu.sqrt();
            for eq in [-root, root] {
                let d = -2.0 * eq;
                println!("saddle_node_normal_form,{:.6},{:.6},{:.6},{},equilibrium_present,Bifurcation interpretation depends on model form parameter meaning and domain validity.", mu, eq, d, classify(d));
            }
        }
    }
}
