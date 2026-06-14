struct Scenario { name: &'static str, initial_state: f64, rate: f64, capacity: f64, time_horizon: f64 }

fn validate_domain(s: &Scenario) -> Option<&'static str> {
    if s.initial_state < 0.0 { return Some("initial_state must be nonnegative"); }
    if s.rate < 0.0 { return Some("rate must be nonnegative"); }
    if s.capacity <= 0.0 { return Some("capacity must be positive"); }
    if s.time_horizon < 0.0 { return Some("time_horizon must be nonnegative"); }
    if s.initial_state > s.capacity { return Some("initial_state exceeds capacity"); }
    None
}

fn bounded_growth(s: &Scenario) -> f64 {
    s.capacity / (1.0 + ((s.capacity - s.initial_state) / s.initial_state) * (-s.rate * s.time_horizon).exp())
}

fn main() {
    let scenarios = [
        Scenario { name: "baseline", initial_state: 10.0, rate: 0.20, capacity: 100.0, time_horizon: 20.0 },
        Scenario { name: "near_capacity", initial_state: 95.0, rate: 0.20, capacity: 100.0, time_horizon: 20.0 },
        Scenario { name: "invalid_negative_state", initial_state: -5.0, rate: 0.20, capacity: 100.0, time_horizon: 20.0 },
        Scenario { name: "outside_capacity", initial_state: 120.0, rate: 0.20, capacity: 100.0, time_horizon: 20.0 },
    ];
    println!("scenario,status,value_or_issue");
    for s in &scenarios {
        match validate_domain(s) {
            Some(issue) => println!("{},domain_review,{}", s.name, issue),
            None => println!("{},ok,{:.6}", s.name, bounded_growth(s)),
        }
    }
}
