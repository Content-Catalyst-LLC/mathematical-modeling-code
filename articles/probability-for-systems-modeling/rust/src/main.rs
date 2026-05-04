use rand::rngs::StdRng;
use rand::{Rng, SeedableRng};

fn main() {
    let n = 10_000;
    let mut rng = StdRng::seed_from_u64(42);
    let mut total = 0.0;

    for _ in 0..n {
        let exposure: f64 = rng.gen_range(0.2..1.0);
        let vulnerability: f64 = rng.gen_range(0.0..1.0);
        let loss = exposure * vulnerability;
        total += loss;
    }

    println!("Monte Carlo mean loss estimate: {:.8}", total / n as f64);
}
