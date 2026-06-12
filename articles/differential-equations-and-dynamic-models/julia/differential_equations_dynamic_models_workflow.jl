# Julia workflow for differential equations and dynamic models.
# Dependency-light: Base and standard library only.

using Printf
using Statistics

struct DynamicScenario
    name::String
    initial_storage::Float64
    capacity::Float64
    inflow_rate::Float64
    demand_rate::Float64
    loss_rate::Float64
    dt::Float64
    horizon::Float64
end

function derivative(storage::Float64, s::DynamicScenario)
    return s.inflow_rate - s.demand_rate - s.loss_rate * storage
end

function simulate_euler(s::DynamicScenario)
    storage = s.initial_storage
    time = 0.0
    steps = Int(round(s.horizon / s.dt))
    rows = Vector{NamedTuple}()

    for step in 0:steps
        rate = derivative(storage, s)
        raw_next = storage + s.dt * rate
        shortage = max(0.0, -raw_next)
        overflow = max(0.0, raw_next - s.capacity)
        next_storage = min(s.capacity, max(0.0, raw_next))

        push!(rows, (
            scenario=s.name,
            step=step,
            time=time,
            storage=storage,
            rate=rate,
            shortage=shortage,
            overflow=overflow
        ))

        storage = next_storage
        time += s.dt
    end

    return rows
end

function main()
    scenarios = [
        DynamicScenario("julia_baseline", 80.0, 100.0, 8.0, 6.0, 0.015, 0.25, 60.0),
        DynamicScenario("julia_high_demand", 80.0, 100.0, 8.0, 10.0, 0.015, 0.25, 60.0),
        DynamicScenario("julia_high_loss", 80.0, 100.0, 8.0, 6.0, 0.050, 0.25, 60.0)
    ]

    for scenario in scenarios
        rows = simulate_euler(scenario)
        storage = [row.storage for row in rows]
        rates = [row.rate for row in rows]
        shortage = [row.shortage for row in rows]
        @printf("%s final_storage=%.3f mean_storage=%.3f mean_rate=%.3f total_shortage=%.3f\n",
                scenario.name, storage[end], mean(storage), mean(rates), sum(shortage))
    end
end

main()
