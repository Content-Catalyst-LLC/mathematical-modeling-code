function exponential_population(n0, r, t)
    return n0 * exp(r * t)
end

function logistic_population(n0, r, k, t)
    return k / (1 + ((k - n0) / n0) * exp(-r * t))
end

n0 = 100.0
r = 0.08
k = 1000.0

println("time,exponential,logistic")
for t in 0:40
    println("$(t),$(exponential_population(n0, r, t)),$(logistic_population(n0, r, k, t))")
end
