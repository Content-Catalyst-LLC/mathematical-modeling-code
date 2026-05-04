# Linear Algebra for Systems Modeling in Julia
# Educational example only.

using LinearAlgebra
using Statistics

A = [
    0.82 0.10 0.08;
    0.12 0.76 0.12;
    0.06 0.18 0.76
]

x = [0.70, 0.20, 0.10]

for t in 1:10
    global x = A * x
end

eigen_results = eigen(A)

println("State after 10 transformations:")
println(x)

println("Eigenvalues:")
println(eigen_results.values)
