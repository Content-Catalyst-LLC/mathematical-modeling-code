"""
Inverse Matrices and Structural Recovery

A small 2x2 example showing how an inverse matrix recovers a hidden state
from an observed output.
"""

def inverse_2x2(a):
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    if det == 0:
        raise ValueError("Matrix is singular; structural recovery is not unique.")
    return [
        [a[1][1] / det, -a[0][1] / det],
        [-a[1][0] / det, a[0][0] / det],
    ]

def matvec(a, x):
    return [
        a[0][0] * x[0] + a[0][1] * x[1],
        a[1][0] * x[0] + a[1][1] * x[1],
    ]

A = [[3, 1], [2, 4]]
x_original = [2, 1]
b = matvec(A, x_original)

A_inv = inverse_2x2(A)
x_recovered = matvec(A_inv, b)

print("A =", A)
print("Original state x =", x_original)
print("Observed output b = Ax =", b)
print("Recovered state A^-1 b =", x_recovered)
