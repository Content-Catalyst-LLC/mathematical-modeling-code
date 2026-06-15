system_response(x) = exp(0.2 * x)
exact_derivative(x) = 0.2 * exp(0.2 * x)
average_rate(a, b) = (system_response(b) - system_response(a)) / (b - a)
forward_difference(x, h) = (system_response(x + h) - system_response(x)) / h
backward_difference(x, h) = (system_response(x) - system_response(x - h)) / h
central_difference(x, h) = (system_response(x + h) - system_response(x - h)) / (2h)
elasticity(d, x) = (x / system_response(x)) * d

x0 = 5.0
h_values = [1.0, 0.5, 0.25, 0.125, 0.0625]
exact = exact_derivative(x0)

println("method,x0,h,estimate,exact,absolute_error,elasticity")
for h in h_values
    rows = [
        ("average_rate_right", average_rate(x0, x0 + h)),
        ("forward_difference", forward_difference(x0, h)),
        ("backward_difference", backward_difference(x0, h)),
        ("central_difference", central_difference(x0, h))
    ]
    for (method, estimate) in rows
        println("$method,$x0,$h,$estimate,$exact,$(abs(estimate - exact)),$(elasticity(estimate, x0))")
    end
end
