# Dependency-light Julia difference-quotient workflow.

system_response(x) = exp(0.2 * x)
exact_derivative(x) = 0.2 * exp(0.2 * x)
difference_quotient(x, h) = (system_response(x + h) - system_response(x)) / h

x0 = 5.0
h_values = [1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001]
exact = exact_derivative(x0)

println("function_name,x,h,estimate,exact_value,absolute_error")
for h in h_values
    estimate = difference_quotient(x0, h)
    println("exp(0.2x),$(x0),$(h),$(estimate),$(exact),$(abs(estimate - exact))")
end
