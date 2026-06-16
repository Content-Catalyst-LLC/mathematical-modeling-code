fn regeneration(stock: f64, growth_rate: f64, carrying_capacity: f64) -> f64 {
    growth_rate * stock * (1.0 - stock / carrying_capacity)
}
fn extraction(efficiency: f64, effort: f64, stock: f64) -> f64 {
    efficiency * effort * stock
}
fn natural_stock_step(stock: f64, growth_rate: f64, carrying_capacity: f64, harvest: f64, stress: f64, dt: f64) -> f64 {
    (stock + (regeneration(stock, growth_rate, carrying_capacity) - harvest - stress) * dt).max(0.0)
}
fn main() {
    let stock = 80.0;
    let harvest = extraction(0.003, 12.0, stock);
    let next = natural_stock_step(stock, 0.08, 100.0, harvest, 0.25, 0.25);
    println!("scenario_name,regeneration,extraction,next_stock,warning");
    println!("baseline_coupled_resource,{:.6},{:.6},{:.6},boundary_human_natural_and_governance_assumptions_required", regeneration(stock,0.08,100.0), harvest, next);
}
