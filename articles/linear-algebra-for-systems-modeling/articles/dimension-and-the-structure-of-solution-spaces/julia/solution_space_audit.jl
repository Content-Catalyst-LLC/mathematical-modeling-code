# Lightweight rank audit for a structured 3 x 4 example.

function matrix_rank_rref(matrix; tolerance=1e-10)
    rows = [matrix[i, :] for i in 1:size(matrix, 1)]
    row_count = length(rows)
    column_count = size(matrix, 2)
    rank = 0

    for column in 1:column_count
        pivot = 0
        for row in (rank + 1):row_count
            if abs(rows[row][column]) > tolerance
                pivot = row
                break
            end
        end
        if pivot == 0
            continue
        end

        rows[rank + 1], rows[pivot] = rows[pivot], rows[rank + 1]
        pivot_value = rows[rank + 1][column]
        rows[rank + 1] = rows[rank + 1] ./ pivot_value

        for row in 1:row_count
            if row != rank + 1
                factor = rows[row][column]
                rows[row] = rows[row] .- factor .* rows[rank + 1]
            end
        end
        rank += 1
    end
    return rank
end

coefficient_matrix = [
    1.0 1.0 0.0 0.0;
    0.0 1.0 1.0 0.0;
    0.0 0.0 1.0 1.0
]

variable_count = size(coefficient_matrix, 2)
equation_count = size(coefficient_matrix, 1)
rank_value = matrix_rank_rref(coefficient_matrix)
nullity_value = variable_count - rank_value

println("system_name,variable_count,equation_count,rank,nullity,likely_solution_structure,warning")
println(join((
    "four_variable_three_constraint_system",
    variable_count,
    equation_count,
    rank_value,
    nullity_value,
    "Positive-dimensional solution space if the system is consistent.",
    "Rank and nullity are mathematical diagnostics not proof of feasibility."
), ","))
