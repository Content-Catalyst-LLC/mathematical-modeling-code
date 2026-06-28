fn main() {
    let a: f64 = 0.80;
    let b: f64 = 0.15;
    let c: f64 = 0.20;
    let d: f64 = 0.90;
    let trace = a + d;
    let determinant = a * d - b * c;
    let discriminant = trace * trace - 4.0 * determinant;
    let root = discriminant.sqrt();
    let lambda_1 = (trace + root) / 2.0;
    let lambda_2 = (trace - root) / 2.0;
    let dominant = lambda_1.abs().max(lambda_2.abs());
    println!("model_name,rank,determinant,dominant_eigenvalue,warning");
    println!("two_component_transition_model,2,{:.6},{:.6},Matrix interpretation depends on entry meaning and scale.", determinant, dominant);
}
