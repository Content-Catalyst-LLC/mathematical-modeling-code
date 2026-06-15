response_function(x) = 10.0 * sqrt(x + 1.0)
analytic_derivative(x) = 5.0 / sqrt(x + 1.0)
finite_difference_derivative(x; h=1e-5) = (response_function(x+h) - response_function(x-h)) / (2h)

function classify_response(e)
    if isnothing(e)
        return "elasticity undefined"
    elseif abs(e) < 1.0
        return "inelastic local response"
    elseif abs(e) == 1.0
        return "unit elastic local response"
    else
        return "elastic local response"
    end
end

println("x,value,derivative,elasticity,finite_difference_derivative,absolute_error,response_class,warning")
for x in [0.0, 0.5, 1.0, 4.0, 9.0, 24.0]
    y = response_function(x)
    d = analytic_derivative(x)
    fd = finite_difference_derivative(x)
    err = abs(d - fd)
    e = (x == 0.0 || y == 0.0) ? nothing : (x / y) * d
    warning = x == 0.0 ? "input is zero; proportional input change requires care" : ""
    eout = isnothing(e) ? "NA" : string(e)
    println("$x,$y,$d,$eout,$fd,$err,$(classify_response(e)),$warning")
end
