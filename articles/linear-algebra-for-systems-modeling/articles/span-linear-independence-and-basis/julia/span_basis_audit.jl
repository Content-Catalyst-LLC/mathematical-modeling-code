function determinant3x3(m)
    return m[1,1]*(m[2,2]*m[3,3] - m[2,3]*m[3,2]) -
           m[1,2]*(m[2,1]*m[3,3] - m[2,3]*m[3,1]) +
           m[1,3]*(m[2,1]*m[3,2] - m[2,2]*m[3,1])
end

matrix = [
    1.0 0.0 0.5;
    0.0 1.0 0.5;
    0.0 0.0 1.0
]

ambient_dimension = 3
vector_count = 3
det_value = determinant3x3(matrix)
rank_value = abs(det_value) > 1e-10 ? 3 : 2
spans = rank_value == ambient_dimension
independent = rank_value == vector_count
basis = spans && independent

println("vector_set_name,ambient_dimension,vector_count,rank,spans_ambient_space,linearly_independent,is_basis_for_ambient_space,warning")
println(join((
    "candidate_system_basis",
    ambient_dimension,
    vector_count,
    rank_value,
    spans,
    independent,
    basis,
    "A mathematical basis claim does not prove real-world adequacy."
), ","))
