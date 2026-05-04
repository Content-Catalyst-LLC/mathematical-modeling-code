# Mathematical Modeling: Logistic Growth in Julia
# Educational example only.

function simulate_logistic(initial_state, growth_rate, carrying_capacity, time_steps)
    state = zeros(time_steps)
    state[1] = initial_state

    for t in 2:time_steps
        state[t] = state[t - 1] + growth_rate * state[t - 1] * (1 - state[t - 1] / carrying_capacity)
    end

    return state
end

state = simulate_logistic(10.0, 0.18, 100.0, 80)

println("Final state: ", state[end])
