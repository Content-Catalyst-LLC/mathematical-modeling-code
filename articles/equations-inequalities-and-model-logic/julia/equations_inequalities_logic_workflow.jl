# Julia workflow for equations, inequalities, and model logic.
# Dependency-light: Base and standard library only.

using Printf
using Statistics

struct LogicScenario
    name::String
    initial_stock::Float64
    capacity::Float64
    inflow::Float64
    demand::Float64
    loss_rate::Float64
    low_storage_threshold::Float64
    demand_reduction::Float64
    periods::Int
end

function simulate(s::LogicScenario)
    stock = s.initial_stock
    demand = s.demand
    rows = Vector{NamedTuple}()

    for period in 0:s.periods
        losses = s.loss_rate * stock
        raw_next = stock + s.inflow - demand - losses
        shortage = max(0.0, -raw_next)
        overflow = max(0.0, raw_next - s.capacity)
        constrained_next = min(s.capacity, max(0.0, raw_next))
        rule_active = stock < s.low_storage_threshold

        push!(rows, (
            scenario=s.name,
            period=period,
            stock=stock,
            shortage=shortage,
            overflow=overflow,
            rule_active=rule_active
        ))

        if rule_active
            demand = max(0.0, demand - s.demand_reduction)
        end

        stock = constrained_next
    end

    return rows
end

function main()
    scenarios = [
        LogicScenario("julia_baseline", 80.0, 100.0, 8.0, 6.0, 0.015, 35.0, 0.5, 60),
        LogicScenario("julia_stress", 40.0, 60.0, 3.0, 7.0, 0.050, 25.0, 1.0, 60),
        LogicScenario("julia_tight_capacity", 70.0, 75.0, 8.0, 6.0, 0.015, 30.0, 0.5, 60)
    ]

    for scenario in scenarios
        rows = simulate(scenario)
        stocks = [row.stock for row in rows]
        shortages = [row.shortage for row in rows]
        activations = [row.rule_active ? 1 : 0 for row in rows]
        @printf("%s final_stock=%.3f mean_stock=%.3f total_shortage=%.3f logic_activations=%d\n",
                scenario.name, stocks[end], mean(stocks), sum(shortages), sum(activations))
    end
end

main()
