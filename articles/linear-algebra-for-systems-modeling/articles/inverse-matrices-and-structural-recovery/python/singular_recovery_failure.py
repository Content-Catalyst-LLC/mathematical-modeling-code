"""
Singular matrix example.

This shows a failed recovery case: the second row is a multiple of the first,
so the matrix collapses structural information.
"""

def determinant_2x2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]

A = [[2, 4], [1, 2]]
det = determinant_2x2(A)

print("A =", A)
print("det(A) =", det)

if det == 0:
    print("No inverse exists.")
    print("Structural recovery is ambiguous because the transformation loses information.")
