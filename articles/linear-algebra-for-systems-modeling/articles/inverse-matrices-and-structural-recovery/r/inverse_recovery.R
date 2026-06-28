# Inverse Matrices and Structural Recovery

A <- matrix(c(3, 2, 1, 4), nrow = 2)
x_original <- matrix(c(2, 1), nrow = 2)
b <- A %*% x_original

x_recovered <- solve(A) %*% b

print("A:")
print(A)
print("Original state:")
print(x_original)
print("Observed output b = Ax:")
print(b)
print("Recovered state solve(A) %*% b:")
print(x_recovered)
