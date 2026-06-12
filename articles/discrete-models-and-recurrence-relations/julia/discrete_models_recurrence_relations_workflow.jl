# Julia workflow for discrete models and recurrence relations.
# Dependency-light: Base and standard library only.

using Printf
using Statistics

struct RecurrenceScenario
    name::String
    initial_storage::Float64
    initial_demand::Float64
    capacity::Float64
    inflow::Float64
    loss_rate::Float64
    demand_response::Float64
    periods::Int
    adaptive_demand::Bool
end

function simulate(s::RecurrenceScenario)
    storage = s.initial_storage
    demand = s.initial_demand
    rows = Vector{NamedTuple}()

    for period in 0:s.periods
        raw_next = storage + s.inflow - demand - s.loss_rate * storage
        shortage = max(0.0, -raw_next)
        overflow = max(0.0, raw_next - s.capacity)
        next_storage = min(s.capacity, max(0.0, raw_next))

        push!(rows, (
            scenario=s.name,
            period=period,
            storage=storage,
            demand=demand,
            shortage=shortage,
            overflow=overflow
        ))

        if s.adaptive_demand
            demand = max(0.0, demand - s.demand_response * shortage)
        end

        storage = next_storage
    end

    return rows
end

function main()
    scenarios = [
        RecurrenceScenario("julia_baseline", 80.0, 7.0, 100.0, 6.0, 0.015, 0.0, 60, false),
        RecurrenceScenario("julia_high_demand", 80.0, 10.0, 100.0, 6.0, 0.015, 0.0, 60, false),
        RecurrenceScenario("julia_adaptive", 45.0, 10.0, 80.0, 4.0, 0.020, 0.20, 60, true)
    ]

    for scenario in scenarios
        rows = simulate(scenario)
        storage = [row.storage for row in rows]
        demand = [row.demand for row in rows]
        shortage = [row.shortage for row in rows]
        @printf("%s final_storage=%.3f mean_storage=%.3f final_demand=%.3f total_shortage=%.3f\n",
                scenario.name, storage[end], mean(storage), demand[end], sum(shortage))
    end
end

main()
