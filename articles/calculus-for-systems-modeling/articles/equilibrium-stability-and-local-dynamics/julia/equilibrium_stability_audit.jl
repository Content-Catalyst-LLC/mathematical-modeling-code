logistic_derivative(x, growth_rate, carrying_capacity) = growth_rate * (1 - 2 * x / carrying_capacity)
bistable_rate(x, threshold) = x * (1 - x) * (x - threshold)
numerical_derivative(f, x; h=1e-5) = (f(x + h) - f(x - h)) / (2h)

function classify_scalar_stability(derivative_value; tolerance=1e-8)
    if derivative_value < -tolerance
        return "locally_stable"
    elseif derivative_value > tolerance
        return "locally_unstable"
    else
        return "inconclusive_by_linearization"
    end
end

println("scenario,equilibrium,derivative_value,stability,domain_min,domain_max,warning")
for eq in [0.0, 100.0]
    d = logistic_derivative(eq, 0.6, 100.0)
    println(join(("logistic_growth", eq, d, classify_scalar_stability(d), 0.0, 100.0, "Logistic stability assumes fixed carrying capacity and smooth density limitation."), ","))
end

threshold = 0.4
for eq in [0.0, threshold, 1.0]
    d = numerical_derivative(x -> bistable_rate(x, threshold), eq)
    println(join(("bistable_threshold", eq, d, classify_scalar_stability(d), 0.0, 1.0, "Threshold stability depends on the assumed threshold and domain."), ","))
end
