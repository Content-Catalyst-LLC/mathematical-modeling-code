function central_difference(values, time)
    n = length(values)
    deriv = zeros(Float64, n)
    deriv[1] = (values[2] - values[1]) / (time[2] - time[1])
    deriv[n] = (values[n] - values[n-1]) / (time[n] - time[n-1])
    for i in 2:(n-1)
        deriv[i] = (values[i+1] - values[i-1]) / (time[i+1] - time[i-1])
    end
    return deriv
end

time = collect(range(0.0, 20.0, length=401))
factor_a = [100 + 4t + 8sin(0.4t) for t in time]
factor_b = [1.2 + 0.03t + 0.15cos(0.25t) for t in time]
product_y = factor_a .* factor_b

a_prime = central_difference(factor_a, time)
b_prime = central_difference(factor_b, time)
direct_y_prime = central_difference(product_y, time)

contribution_from_a = a_prime .* factor_b
contribution_from_b = factor_a .* b_prime
product_rule_y_prime = contribution_from_a .+ contribution_from_b
residual = direct_y_prime .- product_rule_y_prime

println("Mean absolute residual: ", sum(abs.(residual)) / length(residual))
