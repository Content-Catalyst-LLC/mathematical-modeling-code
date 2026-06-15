fn geometric_sum(a:f64, r:f64, n:usize)->f64{
    let mut total = 0.0;
    for i in 0..n {
        total += a * r.powi(i as i32);
    }
    total
}

fn harmonic_sum(n:usize)->f64{
    let mut total = 0.0;
    for i in 1..=n {
        total += 1.0 / (i as f64);
    }
    total
}

fn main(){
    let geo = geometric_sum(10.0,0.6,25);
    let geo_ref = 10.0 / (1.0 - 0.6);
    let harm = harmonic_sum(10000);
    println!("series_name,n_terms,last_term,partial_sum,reference_value,estimated_error,convergence_classification");
    println!("geometric_r_0.6,25,{:.12},{:.12},{:.12},{:.12},convergent geometric series",10.0_f64*0.6_f64.powi(24),geo,geo_ref,geo_ref-geo);
    println!("harmonic,10000,{:.12},{:.12},,,divergent despite terms approaching zero",1.0/10000.0,harm);
}
