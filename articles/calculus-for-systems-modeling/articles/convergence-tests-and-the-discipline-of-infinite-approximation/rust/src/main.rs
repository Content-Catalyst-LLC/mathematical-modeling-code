fn geometric_sum(a:f64, r:f64, n:usize)->f64{
    let mut total = 0.0;
    for i in 0..n {
        total += a * r.powi(i as i32);
    }
    total
}

fn p_series_sum(p:f64, n:usize)->f64{
    let mut total = 0.0;
    for i in 1..=n {
        total += 1.0 / (i as f64).powf(p);
    }
    total
}

fn main(){
    let geo = geometric_sum(10.0,0.6,25);
    let geo_ref = 10.0 / (1.0 - 0.6);
    let p125 = p_series_sum(1.25,10000);
    let p075 = p_series_sum(0.75,10000);
    println!("series_name,test_used,n_terms,partial_sum,last_term,test_result,estimated_error");
    println!("geometric_r_0.6,geometric-series test,25,{:.12},{:.12},converges by geometric-series test,{:.12}",geo,10.0_f64*0.6_f64.powi(24),geo_ref-geo);
    println!("p_series_1.25,p-series test,10000,{:.12},{:.12},converges,",p125,1.0_f64/10000.0_f64.powf(1.25));
    println!("p_series_0.75,p-series test,10000,{:.12},{:.12},diverges,",p075,1.0_f64/10000.0_f64.powf(0.75));
}
