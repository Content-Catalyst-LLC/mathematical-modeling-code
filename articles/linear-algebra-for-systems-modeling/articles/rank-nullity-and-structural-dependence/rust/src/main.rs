fn main() {
    let row_count = 3;
    let column_count = 3;
    let rank = 3;
    let nullity = column_count - rank;
    let rank_deficient = false;
    let tolerance = 1.0e-10;

    println!("system_name,row_count,column_count,rank,nullity,rank_deficient,pivot_columns,free_columns,tolerance,warning");
    println!(
        "three_constraint_resource_balance_matrix,{},{},{},{},{},0;1;2,none,{:.10},Rank and nullity reveal structure but interpretation depends on model meaning.",
        row_count, column_count, rank, nullity, rank_deficient, tolerance
    );
}
