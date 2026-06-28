# Inverse Matrices and Structural Recovery

A = [3 1; 2 4]
x_original = [2; 1]
b = A * x_original

x_recovered = inv(A) * b

println("A = ", A)
println("Original state x = ", x_original)
println("Observed output b = Ax = ", b)
println("Recovered state inv(A)b = ", x_recovered)
