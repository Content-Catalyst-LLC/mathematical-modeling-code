matrix_values = [
    0.0 2.0 0.0 1.0;
    2.0 0.0 3.0 0.0;
    0.0 3.0 0.0 4.0;
    1.0 0.0 4.0 0.0
]

row_count = size(matrix_values, 1)
column_count = size(matrix_values, 2)
entry_count = row_count * column_count
nonzero_entries = count(!=(0.0), matrix_values)
sparsity_ratio = 1.0 - (nonzero_entries / entry_count)
symmetric_matrix = matrix_values == transpose(matrix_values)
rank_value = 4

println("matrix_name,matrix_role,row_count,column_count,nonzero_entries,sparsity_ratio,symmetric,rank,warning")
println(join((
    "infrastructure_interdependency_matrix",
    "weighted adjacency matrix",
    row_count,
    column_count,
    nonzero_entries,
    round(sparsity_ratio, digits=4),
    symmetric_matrix,
    rank_value,
    "Symmetry should not be assumed unless system relationships are reciprocal."
), ","))
