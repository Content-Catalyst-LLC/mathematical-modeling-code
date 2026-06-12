# Julia workflow for reservoir stock-flow modeling process demonstration.
# Dependency-light: Base and standard libraries only.

using Printf
using Statistics

struct ReservoirScenario
    name::String
    initial_storage::Float64
    capacity::Float64
    base_inflow::Float64
    base_demand::Float64
    demand_growth::Float64
    loss_rate::Float64
    periods::Int
end

function bounded_update(storage, inflow, demand, losses, capacity)
    return min(capacity, max(0.0, storage + inflow - demand - losses))
end

function simulate(s::ReservoirScenario)
    storage = s.initial_storage
    rows = Vector{NamedTuple}()
    for period in 0:s.periods
        demand = s.base_demand * (1.0 + s.demand_growth)^period
        losses = s.loss_rate * storage
        shortage = max(0.0, demand + losses - (storage + s.base_inflow))
        push!(rows, (
            scenario=s.name,
            period=period,
            storage=storage,
            demand=demand,
            inflow=s.base_inflow,
            losses=losses,
            shortage=shortage
        ))
        storage = bounded_update(storage, s.base_inflow, demand, losses, s.capacity)
    end
    return rows
end

function main()
    scenarios = [
        ReservoirScenario("julia_baseline", 80.0, 100.0, 8.0, 6.0, 0.010, 0.015, 60),
        ReservoirScenario("julia_stress", 75.0, 100.0, 5.0, 6.5, 0.030, 0.030, 60)
    ]

    for scenario in scenarios
        rows = simulate(scenario)
        storage = [row.storage for row in rows]
        shortages = [row.shortage for row in rows]
        @printf("%s final_storage=%.3f mean_storage=%.3f total_shortage=%.3f\n",
                scenario.name, storage[end], mean(storage), sum(shortages))
    end
end

main()
