fn main() {
    let row_count = 3;
    let column_count = 3;
    let rank = 3;
    let nullity = 0;
    let input_norm = 120.415946;
    let output_norm = 152.750205;
    let amplification_ratio = output_norm / input_norm;

    println!("system_name,row_count,column_count,input_state,output_state,rank,nullity,input_norm,output_norm,amplification_ratio,warning");
    println!(
        "three_component_system_response,{},{},100.000000;60.000000;30.000000,126.000000;75.500000;42.000000,{},{},{:.6},{:.6},{:.6},Matrix action requires row meanings column meanings units scaling and sensitivity review.",
        row_count, column_count, rank, nullity, input_norm, output_norm, amplification_ratio
    );
}
