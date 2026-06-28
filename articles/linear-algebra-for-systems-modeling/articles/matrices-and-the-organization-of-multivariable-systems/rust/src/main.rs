fn main() {
    let row_count = 4;
    let column_count = 4;
    let nonzero_entries = 8;
    let sparsity_ratio = 0.5;
    let symmetric = true;
    let rank = 4;

    println!("matrix_name,matrix_role,row_count,column_count,nonzero_entries,sparsity_ratio,symmetric,rank,warning");
    println!(
        "infrastructure_interdependency_matrix,weighted adjacency matrix,{},{},{},{:.4},{},{},Symmetry should not be assumed unless system relationships are reciprocal.",
        row_count, column_count, nonzero_entries, sparsity_ratio, symmetric, rank
    );
}
