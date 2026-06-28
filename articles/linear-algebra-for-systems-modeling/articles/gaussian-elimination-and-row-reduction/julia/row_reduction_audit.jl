A = [1.0 1.0 0.0; 0.0 1.0 1.0; 1.0 0.0 1.0]
rank_A = 3
rank_augmented = 3
unknown_count = size(A, 2)
consistent = rank_A == rank_augmented
solution_behavior = consistent && rank_A == unknown_count ? "unique solution" : "review needed"
println("system_name,equation_count,unknown_count,pivot_columns,coefficient_rank,augmented_rank,consistent,solution_behavior,warning")
println(join(("three_constraint_resource_balance_system", size(A, 1), unknown_count, "0,1,2", rank_A, rank_augmented, consistent, solution_behavior, "Row reduction reveals algebraic structure but feasibility requires review."), ","))
