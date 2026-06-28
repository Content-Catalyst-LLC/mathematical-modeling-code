A = [
    1.0 1.0 0.0;
    0.0 1.0 1.0;
    1.0 0.0 1.0
]

b = [100.0, 80.0, 90.0]

rank_A = 3
rank_augmented = 3
unknown_count = size(A, 2)
consistent = rank_A == rank_augmented
solution_behavior = consistent && rank_A == unknown_count ? "unique solution" : "review needed"
pivot_columns = "0,1,2"
free_columns = "none"

println("system_name,equation_count,unknown_count,pivot_columns,free_columns,coefficient_rank,augmented_rank,consistent,solution_behavior,warning")
println(join((
    "three_constraint_resource_balance_system",
    size(A, 1),
    unknown_count,
    pivot_columns,
    free_columns,
    rank_A,
    rank_augmented,
    consistent,
    solution_behavior,
    "Pivot structure reveals algebraic solvability but feasibility requires review."
), ","))
