function geometric_terms(a, r, n_terms)
    return [a * r^n for n in 0:(n_terms-1)]
end

function p_series_terms(p, n_terms)
    return [1.0 / (n^p) for n in 1:n_terms]
end

function audit_geometric(a, r, n_terms)
    terms = geometric_terms(a, r, n_terms)
    partial_sum = sum(terms)
    result = "diverges or lacks geometric convergence"
    estimated_error = ""
    warning = "ratio magnitude is not below one"

    if abs(r) < 1
        reference = a / (1-r)
        estimated_error = string(reference - partial_sum)
        result = "converges by geometric-series test"
        warning = ""
    end

    println("geometric_r_$r,geometric-series test,$n_terms,$partial_sum,$(last(terms)),$result,$estimated_error,fixed term count with geometric tail check,$warning")
end

function audit_p_series(p, n_terms)
    terms = p_series_terms(p, n_terms)
    result = p > 1 ? "converges" : "diverges"
    warning = p > 1 ? "" : "p-series diverges for p less than or equal to one"
    println("p_series_$p,p-series test,$n_terms,$(sum(terms)),$(last(terms)),$result,,fixed term count with p-series classification,$warning")
end

println("series_name,test_used,n_terms,partial_sum,last_term,test_result,estimated_error,stopping_rule,warning")
audit_geometric(10.0, 0.6, 25)
audit_geometric(10.0, 1.05, 25)
audit_p_series(1.25, 10000)
audit_p_series(0.75, 10000)
audit_p_series(1.0, 10000)
