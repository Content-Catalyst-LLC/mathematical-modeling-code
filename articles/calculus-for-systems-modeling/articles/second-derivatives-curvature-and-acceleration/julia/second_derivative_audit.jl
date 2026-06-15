logistic(x) = 1.0 / (1.0 + exp(-x))
first_derivative(x) = (y = logistic(x); y * (1.0 - y))
second_derivative(x) = (y = logistic(x); y * (1.0 - y) * (1.0 - 2.0*y))
curvature(x) = abs(second_derivative(x)) / ((1.0 + first_derivative(x)^2)^(1.5))

function classify_concavity(v)
    if v > 1e-8
        return "concave up"
    elseif v < -1e-8
        return "concave down"
    else
        return "near zero curvature candidate"
    end
end

println("x,value,first_derivative,second_derivative,curvature,concavity")
for x in [-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0]
    y = logistic(x)
    fp = first_derivative(x)
    fpp = second_derivative(x)
    k = curvature(x)
    c = classify_concavity(fpp)
    println("$x,$y,$fp,$fpp,$k,$c")
end
