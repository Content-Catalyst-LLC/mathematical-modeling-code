u(x) = 1.0 + x
u_prime(x) = 1.0
v(x) = exp(-0.3 * x) * sin(x)
v_prime(x) = exp(-0.3 * x) * (cos(x) - 0.3 * sin(x))

function trapezoid_integral(values, points)
    total = 0.0
    for i in 1:(length(points)-1)
        dx = points[i+1] - points[i]
        if dx <= 0
            error("Grid points must be strictly increasing.")
        end
        total += 0.5 * (values[i] + values[i+1]) * dx
    end
    return total
end

a = 0.0
b = 4.0
n = 800
points = collect(range(a, b, length=n+1))

direct_integral = trapezoid_integral([u(x) * v_prime(x) for x in points], points)
residual_integral = trapezoid_integral([v(x) * u_prime(x) for x in points], points)
boundary_term = u(b) * v(b) - u(a) * v(a)
decomposed_value = boundary_term - residual_integral
decomposition_residual = direct_integral - decomposed_value

println("interval_start,interval_end,direct_integral,boundary_term,residual_integral,decomposed_value,decomposition_residual,method")
println("$a,$b,$direct_integral,$boundary_term,$residual_integral,$decomposed_value,$decomposition_residual,trapezoidal comparison")
