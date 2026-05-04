# Calculus for Systems Modeling in Julia
# Educational example only.

function simulate_logistic(initial_state, rate, capacity, dt, steps)
    state = zeros(steps)
    time = zeros(steps)

    state[1] = initial_state

    for i in 2:steps
        derivative = rate * state[i - 1] * (1 - state[i - 1] / capacity)
        state[i] = state[i - 1] + derivative * dt
        time[i] = time[i - 1] + dt
    end

    return time, state
end

time, state = simulate_logistic(10.0, 0.20, 100.0, 0.1, 300)

println("Final state: ", state[end])
