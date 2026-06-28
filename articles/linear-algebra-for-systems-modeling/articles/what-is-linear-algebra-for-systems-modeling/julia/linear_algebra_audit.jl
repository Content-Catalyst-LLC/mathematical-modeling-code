using LinearAlgebra

matrix_system = [0.80 0.15; 0.20 0.90]
rank_value = rank(matrix_system)
determinant_value = det(matrix_system)
eigenvalues = eigvals(matrix_system)
dominant_eigenvalue = maximum(abs.(eigenvalues))

println("model_name,rows,columns,rank,determinant,dominant_eigenvalue,matrix_meaning,interpretation_warning")
println(join((
    "two_component_transition_model",
    size(matrix_system, 1),
    size(matrix_system, 2),
    rank_value,
    determinant_value,
    dominant_eigenvalue,
    "transition-like matrix connecting two system components across a modeling step",
    "Matrix interpretation depends on entries scale and model assumptions."
), ","))
