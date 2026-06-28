fn main() {
    let compatible_shape = true;
    let output_entry_sum = 3.95;

    println!("operation_name,matrix_shape,compatible_shape,output_entry_sum,warning");
    println!(
        "baseline_plus_weighted_intervention_and_stress,3x3,{},{:.4},Shape compatibility is not enough; semantic compatibility must be documented.",
        compatible_shape, output_entry_sum
    );
}
