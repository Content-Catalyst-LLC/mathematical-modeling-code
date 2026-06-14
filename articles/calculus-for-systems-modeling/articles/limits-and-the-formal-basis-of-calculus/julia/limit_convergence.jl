# Dependency-light Julia limit convergence workflow.

f(x) = exp(0.2 * x)
exact_derivative(x) = 0.2 * exp(0.2 * x)
forward_difference(x, h) = (f(x + h) - f(x)) / h
central_difference(x, h) = (f(x + h) - f(x - h)) / (2h)
richardson(central_h, central_h2) = (4.0 * central_h2 - central_h) / 3.0

x0 = 5.0
h_values = [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125]
exact = exact_derivative(x0)

println("method,x,h,estimate,exact,absolute_error")
for h in h_values
    fd = forward_difference(x0, h)
    cd = central_difference(x0, h)
    cd2 = central_difference(x0, h / 2.0)
    rich = richardson(cd, cd2)
    println("forward_difference,$x0,$h,$fd,$exact,$(abs(fd - exact))")
    println("central_difference,$x0,$h,$cd,$exact,$(abs(cd - exact))")
    println("richardson_central,$x0,$h,$rich,$exact,$(abs(rich - exact))")
end
