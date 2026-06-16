exponential(n0, r, t) = n0 * exp(r * t)
logistic(n0, r, k, t) = k / (1 + ((k - n0) / n0) * exp(-r * t))
function simulate(n0, f, dt, steps)
    n = n0
    for _ in 1:steps
        n = max(0.0, n + dt * f(n))
    end
    return n
end
n0 = 100.0; r = 0.08; k = 1000.0; a = 75.0; h = 12.0; dt = 0.1; steps = 400
println("scenario_name,model_type,final_population,warning")
println("exponential_baseline,exponential,$(exponential(n0,r,40.0)),unconstrained baseline")
println("logistic_capacity_limited,logistic,$(logistic(n0,r,k,40.0)),capacity-limited assumption")
println("allee_threshold,allee_effect,$(simulate(n0, n -> r*n*(1-n/k)*(n/a-1), dt, steps)),threshold-dependent recovery")
println("harvesting_pressure,harvesting,$(simulate(n0, n -> r*n*(1-n/k)-h, dt, steps)),management removal assumption")
