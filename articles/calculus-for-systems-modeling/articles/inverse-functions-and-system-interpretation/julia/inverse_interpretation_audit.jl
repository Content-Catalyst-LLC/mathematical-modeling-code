forward_model(x) = log1p(x)
forward_derivative(x) = 1.0 / (1.0 + x)
inverse_model(y) = exp(y) - 1.0

println("target_output,recovered_input,forward_check,residual,forward_derivative,inverse_sensitivity,domain_valid")
for y in [0.0, 0.5, 1.0, 1.5, 2.0]
    x = inverse_model(y)
    ycheck = forward_model(x)
    residual = ycheck - y
    deriv = forward_derivative(x)
    invsens = 1.0 / deriv
    domainvalid = x > -1.0
    println("$y,$x,$ycheck,$residual,$deriv,$invsens,$domainvalid")
end
