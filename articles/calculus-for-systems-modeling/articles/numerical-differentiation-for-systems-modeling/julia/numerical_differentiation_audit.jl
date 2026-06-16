signal_function(x) = sin(x) + 0.1 * x^2
true_derivative(x) = cos(x) + 0.2 * x

start = 0.0
stop = 10.0
h = 0.1
xs = collect(start:h:stop)
values = signal_function.(xs)

println("index,x,value,true_derivative,forward_difference,backward_difference,central_difference,central_absolute_error,step_size,warning")
for i in eachindex(xs)
    forward = i < length(xs) ? (values[i+1] - values[i]) / h : ""
    backward = i > 1 ? (values[i] - values[i-1]) / h : ""
    central = ""
    central_error = ""
    if i > 1 && i < length(xs)
        central_value = (values[i+1] - values[i-1]) / (2*h)
        central = central_value
        central_error = abs(central_value - true_derivative(xs[i]))
    end
    println(join((i-1, xs[i], values[i], true_derivative(xs[i]), forward, backward, central, central_error, h, "Numerical derivatives depend on step size formula choice boundary handling smoothness and noise."), ","))
end
