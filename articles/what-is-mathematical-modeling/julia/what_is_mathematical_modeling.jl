# Julia workflow for a bounded-growth mathematical model.
# Dependency-light: Base and standard library only.

using Printf
using Statistics

struct LogisticModel
    name::String
    initial_state::Float64
    growth_rate::Float64
    carrying_capacity::Float64
    dt::Float64
    steps::Int
end

function derivative(x::Float64, r::Float64, k::Float64)::Float64
    return r * x * (1.0 - x / k)
end

function simulate_rk4(model::LogisticModel)
    x = model.initial_state
    rows = Vector{NamedTuple}()
    for step in 0:model.steps
        t = step * model.dt
        push!(rows, (scenario=model.name, step=step, time=t, state=x))

        k1 = derivative(x, model.growth_rate, model.carrying_capacity)
        k2 = derivative(x + 0.5 * model.dt * k1, model.growth_rate, model.carrying_capacity)
        k3 = derivative(x + 0.5 * model.dt * k2, model.growth_rate, model.carrying_capacity)
        k4 = derivative(x + model.dt * k3, model.growth_rate, model.carrying_capacity)
        x = max(0.0, x + (model.dt / 6.0) * (k1 + 2k2 + 2k3 + k4))
    end
    return rows
end

function main()
    model = LogisticModel("julia_baseline", 10.0, 0.35, 100.0, 0.1, 160)
    rows = simulate_rk4(model)
    states = [row.state for row in rows]
    @printf("Julia logistic model complete\n")
    @printf("Final state: %.6f\n", states[end])
    @printf("Mean state: %.6f\n", mean(states))
end

main()
