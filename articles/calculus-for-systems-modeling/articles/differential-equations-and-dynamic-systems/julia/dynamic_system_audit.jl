exponential_rate(x, r) = r * x
logistic_rate(x, r, capacity) = r * x * (1 - x / capacity)

function simulate_exponential(x0, r, dt, steps)
    x = x0
    rows = []
    for n in 0:steps
        t = n * dt
        rate = exponential_rate(x, r)
        push!(rows, ("exponential_growth", "dx_dt_equals_r_x", t, x, rate, r, "NA", "explicit_euler", "Exponential growth assumes no capacity constraint."))
        x = x + dt * rate
    end
    rows
end

function simulate_logistic(x0, r, capacity, dt, steps)
    x = x0
    rows = []
    for n in 0:steps
        t = n * dt
        rate = logistic_rate(x, r, capacity)
        push!(rows, ("logistic_growth", "dx_dt_equals_r_x_one_minus_x_over_K", t, x, rate, r, capacity, "explicit_euler", "Logistic growth assumes a fixed carrying capacity."))
        x = x + dt * rate
    end
    rows
end

println("scenario,model_type,time,state,rate,growth_rate,carrying_capacity,method,warning")
for row in vcat(simulate_exponential(10.0, 0.35, 0.1, 100), simulate_logistic(10.0, 0.35, 100.0, 0.1, 100))
    println(join(row, ","))
end
