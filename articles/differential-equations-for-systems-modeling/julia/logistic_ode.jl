# Differential Equations for Systems Modeling in Julia
# Logistic ODE simulation using Euler's method.
# Educational example only.

function logistic_rate(state, growth_rate, capacity)
    return growth_rate * state * (1 - state / capacity)
end

function simulate_logistic(initial_state, growth_rate, capacity, dt, steps)
    time = zeros(steps)
    state = zeros(steps)

    state[1] = initial_state

    for i in 2:steps
        derivative = logistic_rate(state[i - 1], growth_rate, capacity)
        state[i] = state[i - 1] + derivative * dt
        time[i] = time[i - 1] + dt
    end

    return time, state
end

time, state = simulate_logistic(10.0, 0.20, 100.0, 0.1, 300)

println("Final state: ", state[end])
println("Maximum state: ", maximum(state))
