# Inverse Matrices and Structural Recovery
# Julia diagnostics: solve, rank, condition number, residuals.

using LinearAlgebra

function recovery_report(A, b, label)
    println("\n=== $label ===")
    println("A = ")
    println(A)
    println("b = ", b)

    println("rank(A) = ", rank(A))
    println("cond(A) = ", cond(A))

    if size(A, 1) == size(A, 2)
        println("det(A) = ", det(A))
    end

    if size(A, 1) == size(A, 2) && rank(A) == size(A, 2)
        x_hat = A \ b
        residual = A * x_hat - b
        println("method = A \\ b")
        println("x_hat = ", x_hat)
        println("residual norm = ", norm(residual))
    else
        x_hat = pinv(A) * b
        residual = A * x_hat - b
        println("method = pinv(A) * b")
        println("x_hat = ", x_hat)
        println("residual norm = ", norm(residual))
    end
end

A = [3.0 1.0; 2.0 4.0]
x_true = [2.0, 1.0]
b = A * x_true
recovery_report(A, b, "well-conditioned square recovery")

A_bad = [1.0 1.0; 1.0 1.0001]
b_bad = A_bad * [1.0, 1.0]
recovery_report(A_bad, b_bad, "near-singular recovery")

A_over = [1.0 0.0; 0.0 1.0; 1.0 1.0; 2.0 -1.0]
b_over = [2.02, 0.97, 3.04, 3.03]
recovery_report(A_over, b_over, "overdetermined sensor recovery")
