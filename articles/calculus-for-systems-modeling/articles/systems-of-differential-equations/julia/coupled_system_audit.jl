function predator_prey_rates(prey, predator, alpha, beta, delta, gamma)
    prey_rate = alpha * prey - beta * prey * predator
    predator_rate = delta * prey * predator - gamma * predator
    prey_rate, predator_rate
end

function simulate_predator_prey(prey0, predator0, alpha, beta, delta, gamma, dt, steps)
    prey = prey0
    predator = predator0
    rows = []
    for n in 0:steps
        t = n * dt
        prey_rate, predator_rate = predator_prey_rates(prey, predator, alpha, beta, delta, gamma)
        push!(rows, ("predator_prey_coupled_system", t, prey, predator, prey_rate, predator_rate, alpha, beta, delta, gamma, "explicit_euler", "Predator-prey terms are illustrative and assume continuous well-mixed interaction."))
        prey = max(0.0, prey + dt * prey_rate)
        predator = max(0.0, predator + dt * predator_rate)
    end
    rows
end

println("scenario,time,prey,predator,prey_rate,predator_rate,alpha,beta,delta,gamma,method,warning")
for row in simulate_predator_prey(40.0, 9.0, 0.7, 0.05, 0.02, 0.5, 0.01, 2000)
    println(join(row, ","))
end
