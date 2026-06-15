logistic_rate(x, growth_rate, carrying_capacity) = growth_rate * x * (1 - x / carrying_capacity)
bistable_rate(x, threshold) = x * (1 - x) * (x - threshold)

function simulate_scalar(scenario, x0, dt, steps, rate_function, parameters, warning)
    x = x0
    rows = []
    for n in 0:steps
        t = n * dt
        rate = rate_function(x)
        push!(rows, (scenario, t, x, rate, parameters[1], parameters[2], parameters[3], "explicit_euler", warning))
        x = x + dt * rate
    end
    rows
end

println("scenario,time,state,rate,parameter_a,parameter_b,parameter_c,method,warning")
for row in vcat(
    simulate_scalar("logistic_growth", 10.0, 0.05, 300, x -> logistic_rate(x, 0.6, 100.0), (0.6, 100.0, 0.0), "Logistic growth assumes a fixed carrying capacity and smooth density limitation."),
    simulate_scalar("bistable_threshold", 0.35, 0.05, 300, x -> bistable_rate(x, 0.4), (0.4, 0.0, 0.0), "Threshold behavior is illustrative and should not be interpreted without evidence for the threshold.")
)
    println(join(row, ","))
end
