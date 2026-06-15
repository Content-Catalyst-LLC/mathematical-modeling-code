g(x) = x^2 + 1.0
g_prime(x) = 2.0 * x
f(u) = sqrt(u)
integrand_x(x) = f(g(x)) * g_prime(x)

function trapezoid_integral(values, points)
    total = 0.0
    for i in 1:(length(points)-1)
        step = points[i+1] - points[i]
        if step <= 0
            error("Grid points must be strictly increasing.")
        end
        total += 0.5 * (values[i] + values[i+1]) * step
    end
    return total
end

a = 1.0
b = 3.0
n = 400

x_points = collect(range(a, b, length=n+1))
direct_integral = trapezoid_integral([integrand_x(x) for x in x_points], x_points)

u_start = g(a)
u_end = g(b)
u_points = collect(range(u_start, u_end, length=n+1))
transformed_integral = trapezoid_integral([f(u) for u in u_points], u_points)

residual = direct_integral - transformed_integral

println("original_start,original_end,transformed_start,transformed_end,direct_integral,transformed_integral,residual,method")
println("$a,$b,$u_start,$u_end,$direct_integral,$transformed_integral,$residual,trapezoidal comparison")
