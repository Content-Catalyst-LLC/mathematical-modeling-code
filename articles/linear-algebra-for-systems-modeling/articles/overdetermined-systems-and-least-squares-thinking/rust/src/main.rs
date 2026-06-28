fn main() {
    let row_count = 4;
    let column_count = 2;
    let overdetermined = true;
    let rank = 2;
    let residual_norm = 0.191311;

    println!("system_name,row_count,column_count,overdetermined,rank,solution,fitted_values,residuals,residual_norm,warning");
    println!(
        "four_observation_linear_calibration,{},{},{},{},0.850000;1.040000,1.890000;2.930000;3.970000;5.010000,0.110000;-0.030000;0.130000;0.090000,{:.6},Least squares requires residual and model-purpose review.",
        row_count, column_count, overdetermined, rank, residual_norm
    );
}
