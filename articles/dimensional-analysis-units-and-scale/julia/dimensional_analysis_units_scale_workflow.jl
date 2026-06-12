# Julia workflow for dimensional analysis, units, and scale.
# Dependency-light: Base and standard library only.

using Printf
using Statistics

struct ScaleScenario
    name::String
    initial_storage::Float64
    capacity::Float64
    inflow_per_day::Float64
    demand_per_day::Float64
    loss_rate_per_day::Float64
    delta_t_days::Float64
    periods::Int
end

function simulate(s::ScaleScenario)
    storage = s.initial_storage
    rows = Vector{NamedTuple}()

    for period in 0:s.periods
        inflow_volume = s.delta_t_days * s.inflow_per_day
        demand_volume = s.delta_t_days * s.demand_per_day
        loss_volume = s.delta_t_days * s.loss_rate_per_day * storage
        raw_next = storage + inflow_volume - demand_volume - loss_volume
        shortage = max(0.0, -raw_next)
        overflow = max(0.0, raw_next - s.capacity)
        next_storage = min(s.capacity, max(0.0, raw_next))
        storage_fraction = next_storage / s.capacity

        push!(rows, (
            scenario=s.name,
            period=period,
            storage=storage,
            shortage=shortage,
            overflow=overflow,
            storage_fraction=storage_fraction
        ))

        storage = next_storage
    end

    return rows
end

function main()
    scenarios = [
        ScaleScenario("julia_daily_baseline", 80.0, 100.0, 8.0, 6.0, 0.015, 1.0, 60),
        ScaleScenario("julia_weekly_step", 80.0, 100.0, 8.0, 6.0, 0.015, 7.0, 12),
        ScaleScenario("julia_tight_capacity", 70.0, 75.0, 8.0, 6.0, 0.015, 1.0, 60)
    ]

    for scenario in scenarios
        rows = simulate(scenario)
        fractions = [row.storage_fraction for row in rows]
        shortages = [row.shortage for row in rows]
        @printf("%s final_fraction=%.3f min_fraction=%.3f max_fraction=%.3f total_shortage=%.3f\n",
                scenario.name, fractions[end], minimum(fractions), maximum(fractions), sum(shortages))
    end
end

main()
