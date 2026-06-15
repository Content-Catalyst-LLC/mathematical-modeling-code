logistic_map(x, r) = r * x * (1 - x)
logistic_derivative(x, r) = r * (1 - 2 * x)

function estimate_lyapunov(x0, r, burn_in, sample_steps)
    x = x0
    for _ in 1:burn_in
        x = logistic_map(x, r)
    end
    values = Float64[]
    for _ in 1:sample_steps
        derivative_value = abs(logistic_derivative(x, r))
        if derivative_value > 0
            push!(values, log(derivative_value))
        end
        x = logistic_map(x, r)
    end
    mean(values)
end

r = 3.9
x_reference = 0.2
x_perturbed = 0.2 + 1e-8

println("step,x_reference,x_perturbed,absolute_difference,log_difference,warning")
for step in 0:100
    difference = abs(x_reference - x_perturbed)
    log_difference = difference > 0 ? log(difference) : ""
    println(join((step, x_reference, x_perturbed, difference, log_difference, "Trajectory divergence depends on parameter value initial uncertainty numerical precision and iteration count."), ","))
    global x_reference = logistic_map(x_reference, r)
    global x_perturbed = logistic_map(x_perturbed, r)
end
