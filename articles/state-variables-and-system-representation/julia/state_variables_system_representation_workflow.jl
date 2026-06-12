# Julia workflow for state variables and system representation.
# Dependency-light: Base and standard library only.

using Printf
using Statistics

struct RepresentationScenario
    name::String
    representation::String
    initial_storage::Float64
    initial_demand::Float64
    initial_condition::Float64
    capacity::Float64
    inflow::Float64
    loss_rate::Float64
    demand_response::Float64
    condition_decay::Float64
    periods::Int
end

function simulate(s::RepresentationScenario)
    storage = s.initial_storage
    demand = s.initial_demand
    condition = s.initial_condition
    rows = Vector{NamedTuple}()

    for period in 0:s.periods
        effective_loss = s.loss_rate
        if s.representation == "condition_aware"
            effective_loss = s.loss_rate * (1.0 + (1.0 - condition))
        end

        losses = effective_loss * storage
        raw_next = storage + s.inflow - demand - losses
        shortage = max(0.0, -raw_next)
        overflow = max(0.0, raw_next - s.capacity)
        next_storage = min(s.capacity, max(0.0, raw_next))

        push!(rows, (
            scenario=s.name,
            representation=s.representation,
            period=period,
            storage=storage,
            demand=demand,
            condition=condition,
            shortage=shortage,
            overflow=overflow
        ))

        if s.representation == "adaptive_demand" || s.representation == "condition_aware"
            demand = max(0.0, demand - s.demand_response * shortage)
        end

        if s.representation == "condition_aware"
            condition = max(0.0, condition - s.condition_decay * (shortage + overflow))
        end

        storage = next_storage
    end

    return rows
end

function main()
    scenarios = [
        RepresentationScenario("julia_storage_only", "storage_only", 80.0, 7.0, 1.0, 100.0, 6.0, 0.015, 0.0, 0.0, 60),
        RepresentationScenario("julia_adaptive", "adaptive_demand", 45.0, 8.0, 1.0, 80.0, 4.0, 0.020, 0.20, 0.0, 60),
        RepresentationScenario("julia_condition", "condition_aware", 45.0, 8.0, 0.85, 80.0, 4.0, 0.020, 0.20, 0.002, 60)
    ]

    for scenario in scenarios
        rows = simulate(scenario)
        storage = [row.storage for row in rows]
        shortage = [row.shortage for row in rows]
        condition = [row.condition for row in rows]
        @printf("%s representation=%s final_storage=%.3f mean_storage=%.3f final_condition=%.3f total_shortage=%.3f\n",
                scenario.name, scenario.representation, storage[end], mean(storage), condition[end], sum(shortage))
    end
end

main()
