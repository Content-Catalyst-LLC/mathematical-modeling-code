function taylor_exp_maclaurin(x, order)
    total = 0.0
    for n in 0:order
        total += (x^n) / factorial(big(n))
    end
    return Float64(total)
end

function audit_exp(x, order)
    approximation = taylor_exp_maclaurin(x, order)
    reference = exp(x)
    absolute_error = abs(reference - approximation)
    relative_error = absolute_error / abs(reference)
    warning = abs(x) <= 2 ? "" : "Evaluation is far from the expansion center; review local validity."
    println("Maclaurin truncation,exp(x),0.0,$x,$order,$approximation,$reference,$absolute_error,$relative_error,$warning")
end

println("method,function_name,center,x_value,order,approximation,reference_value,absolute_error,relative_error,warning")
audit_exp(0.5, 2)
audit_exp(0.5, 5)
audit_exp(1.0, 10)
audit_exp(3.0, 10)
