# Differential Equations for Systems Modeling in Julia
# Predator-prey coupled system.
# Educational example only.

function simulate_predator_prey(alpha, beta, delta, gamma, initial_prey, initial_predator, dt, steps)
    time = zeros(steps)
    prey = zeros(steps)
    predator = zeros(steps)

    prey[1] = initial_prey
    predator[1] = initial_predator

    for i in 2:steps
        dx = alpha * prey[i - 1] - beta * prey[i - 1] * predator[i - 1]
        dy = delta * prey[i - 1] * predator[i - 1] - gamma * predator[i - 1]

        prey[i] = max(prey[i - 1] + dx * dt, 0.0)
        predator[i] = max(predator[i - 1] + dy * dt, 0.0)
        time[i] = time[i - 1] + dt
    end

    return time, prey, predator
end

time, prey, predator = simulate_predator_prey(1.10, 0.40, 0.10, 0.40, 10.0, 5.0, 0.01, 5000)

println("Final prey: ", prey[end])
println("Final predator: ", predator[end])
