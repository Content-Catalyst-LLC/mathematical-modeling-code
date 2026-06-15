#[derive(Debug)]
struct ProductContribution {
    contribution_from_a: f64,
    contribution_from_b: f64,
    total_derivative: f64,
}

fn product_rule(a: f64, b: f64, da: f64, db: f64) -> ProductContribution {
    let contribution_from_a = da * b;
    let contribution_from_b = a * db;
    ProductContribution { contribution_from_a, contribution_from_b, total_derivative: contribution_from_a + contribution_from_b }
}

fn main() {
    println!("{:?}", product_rule(120.0, 1.5, 4.0, 0.03));
}
