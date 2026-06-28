A = [
    1.0 1.0 0.0;
    0.0 1.0 1.0;
    1.0 0.0 1.0
]

row_count = size(A, 1)
column_count = size(A, 2)
rank_value = 3
nullity_value = column_count - rank_value
rank_deficient = rank_value < min(row_count, column_count)

println("system_name,row_count,column_count,rank,nullity,rank_deficient,pivot_columns,free_columns,warning")
println(join((
    "three_constraint_resource_balance_matrix",
    row_count,
    column_count,
    rank_value,
    nullity_value,
    rank_deficient,
    "0;1;2",
    "none",
    "Rank and nullity reveal structure but interpretation depends on model meaning."
), ","))
