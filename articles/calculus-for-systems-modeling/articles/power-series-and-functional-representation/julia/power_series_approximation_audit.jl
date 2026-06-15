function geometric_power_series(x, n_terms)
    total = 0.0
    for n in 0:(n_terms-1)
        total += x^n
    end
    return total
end

function audit_geometric_series(x, n_terms)
    partial = geometric_power_series(x, n_terms)
    converges = abs(x) < 1
    reference = converges ? 1.0 / (1.0 - x) : missing
    error = converges ? abs(reference - partial) : missing
    status = converges ? "inside radius of convergence" : "outside radius of convergence"
    warning = converges ? "" : "Power series does not converge for this x value."
    println("1/(1-x),0.0,$x,$n_terms,$partial,$reference,$error,$status,$warning")
end

println("function_name,center,x_value,n_terms,partial_sum,reference_value,absolute_error,convergence_status,warning")
audit_geometric_series(0.25, 5)
audit_geometric_series(0.25, 10)
audit_geometric_series(0.75, 5)
audit_geometric_series(0.75, 20)
audit_geometric_series(1.25, 10)
