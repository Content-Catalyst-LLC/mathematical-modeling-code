# Scientific Computing for Systems Modeling in Julia
# Educational example only.

function trapezoid_integral(x, y)
    total = 0.0
    for i in 2:length(x)
        width = x[i] - x[i - 1]
        total += 0.5 * (y[i] + y[i - 1]) * width
    end
    return total
end

function bisection_root(f, lower, upper; tolerance=1e-8, max_iter=100)
    f_lower = f(lower)
    f_upper = f(upper)

    if f_lower * f_upper > 0
        error("Bisection requires a sign change.")
    end

    for _ in 1:max_iter
        midpoint = 0.5 * (lower + upper)
        f_mid = f(midpoint)

        if abs(f_mid) < tolerance
            return midpoint
        end

        if f_lower * f_mid < 0
            upper = midpoint
            f_upper = f_mid
        else
            lower = midpoint
            f_lower = f_mid
        end
    end

    return 0.5 * (lower + upper)
end

x = range(0, 10, length=501)
y = [sin(v) + 1.5 for v in x]

integral_estimate = trapezoid_integral(collect(x), y)
root_estimate = bisection_root(z -> z^2 - 2.0, 0.0, 2.0)

println("Trapezoid integral estimate: ", integral_estimate)
println("Bisection root estimate: ", root_estimate)
