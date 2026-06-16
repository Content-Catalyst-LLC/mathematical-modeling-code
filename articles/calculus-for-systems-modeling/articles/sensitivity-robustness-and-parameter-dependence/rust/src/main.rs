struct Record {
    parameter: &'static str,
    baseline: f64,
    lower: f64,
    upper: f64,
    status: &'static str,
    warning: &'static str,
}

fn main() {
    let records = [
        Record { parameter: "growth_rate", baseline: 0.35, lower: 0.20, upper: 0.50, status: "sensitive", warning: "conclusion may depend on growth-rate assumptions" },
        Record { parameter: "carrying_capacity", baseline: 100.0, lower: 75.0, upper: 125.0, status: "sensitive", warning: "capacity scale affects final stock interpretation" },
        Record { parameter: "initial_stock", baseline: 10.0, lower: 5.0, upper: 20.0, status: "stable", warning: "output variation is limited across this synthetic range" },
    ];
    println!("parameter_name,baseline_value,lower_bound,upper_bound,status,warning");
    for r in records {
        println!("{},{},{},{},{},{}", r.parameter, r.baseline, r.lower, r.upper, r.status, r.warning);
    }
}
