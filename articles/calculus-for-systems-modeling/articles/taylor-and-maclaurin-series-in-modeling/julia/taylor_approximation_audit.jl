function taylor_exp_maclaurin(x, order)
    total = 0.0
    for n in 0:order
        total += (x^n) / factorial(big(n))
    end
    return Float64(total)
end

function taylor_sin_maclaurin(x, order)
    total = 0.0
    for n in 0:order
        total += ((-1)^n) * (x^(2*n + 1)) / factorial(big(2*n + 1))
    end
    return Float64(total)
end

function audit(name, x, order, approximation, reference)
    error = abs(reference - approximation)
    warning = abs(x) <= 2 ? "" : "Evaluation is far from the Maclaurin center; review truncation error carefully."
    println("$name,0.0,$x,$order,$approximation,$reference,$error,$warning")
end

println("function_name,center,x_value,order,approximation,reference_value,absolute_error,warning")
audit("exp(x)", 0.5, 2, taylor_exp_maclaurin(0.5,2), exp(0.5))
audit("exp(x)", 1.0, 10, taylor_exp_maclaurin(1.0,10), exp(1.0))
audit("exp(x)", 3.0, 10, taylor_exp_maclaurin(3.0,10), exp(3.0))
audit("sin(x)", 1.0, 5, taylor_sin_maclaurin(1.0,5), sin(1.0))
audit("sin(x)", 3.0, 10, taylor_sin_maclaurin(3.0,10), sin(3.0))
