tail_function(x) = exp(-0.4 * x)
exact_reference() = 1.0 / 0.4

function trapezoid_integral(func, a, b, n)
    if b <= a
        error("Upper bound must exceed lower bound.")
    end
    dx = (b-a)/n
    total = 0.0
    for i in 0:(n-1)
        x0 = a + i*dx
        x1 = x0 + dx
        total += 0.5 * (func(x0) + func(x1)) * dx
    end
    return total
end

cutoffs = [2.0, 4.0, 8.0, 12.0, 20.0]
reference = exact_reference()

println("cutoff,truncated_value,reference_value,tail_error,method")
for cutoff in cutoffs
    truncated = trapezoid_integral(tail_function, 0.0, cutoff, 4000)
    tail_error = reference - truncated
    println("$cutoff,$truncated,$reference,$tail_error,trapezoidal truncation audit")
end
