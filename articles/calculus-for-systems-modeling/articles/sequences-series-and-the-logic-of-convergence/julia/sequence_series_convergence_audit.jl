function geometric_terms(a, r, n_terms)
    return [a * r^n for n in 0:(n_terms-1)]
end

function harmonic_terms(n_terms)
    return [1.0 / n for n in 1:n_terms]
end

function audit_geometric(a, r, n_terms)
    terms = geometric_terms(a, r, n_terms)
    partial_sum = sum(terms)
    reference_value = ""
    estimated_error = ""
    classification = "divergent or inconclusive"
    warning = ""

    if abs(r) < 1
        reference = a / (1 - r)
        error = reference - partial_sum
        reference_value = string(reference)
        estimated_error = string(error)
        classification = "convergent geometric series"
    else
        warning = "geometric ratio does not support convergence"
    end

    println("geometric_r_$r,$n_terms,$(last(terms)),$partial_sum,$reference_value,$estimated_error,$classification,fixed term count with analytic tail check,$warning")
end

function audit_harmonic(n_terms)
    terms = harmonic_terms(n_terms)
    println("harmonic,$n_terms,$(last(terms)),$(sum(terms)),,,divergent despite terms approaching zero,fixed term count; no finite limiting total,small last term does not imply finite accumulated total")
end

println("series_name,n_terms,last_term,partial_sum,reference_value,estimated_error,convergence_classification,stopping_rule,warning")
audit_geometric(10.0, 0.6, 25)
audit_geometric(10.0, 1.05, 25)
audit_harmonic(10000)
