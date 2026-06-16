fn linear_decline(e0: f64, year: usize, years: usize) -> f64 {
    f64::max(0.0, e0 * (1.0 - (year as f64 / years as f64)))
}

fn main() {
    let e0 = 40.0;
    let years = 30usize;
    let cumulative: f64 = (0..=years).map(|y| linear_decline(e0, y, years)).sum();
    println!("scenario_name,pathway_type,cumulative_emissions,warning");
    println!("linear_decline_to_zero,linear_decline,{:.6},linear_decline_still_accumulates_until_net_zero", cumulative);
}
