# Julia workflow for boundary, scale, and scope scenario review.
# Dependency-light: Base and standard library only.

using Printf
using Statistics

struct BoundaryScenario
    name::String
    boundary_version::String
    initial_stock::Float64
    capacity::Float64
    inflow::Float64
    demand::Float64
    loss_rate::Float64
    policy_savings::Float64
    periods::Int
end

function bounded_update(stock, inflow, demand, losses, capacity)
    return min(capacity, max(0.0, stock + inflow - demand - losses))
end

function simulate(s::BoundaryScenario)
    stock = s.initial_stock
    rows = Vector{NamedTuple}()
    for period in 0:s.periods
        effective_demand = max(0.0, s.demand - s.policy_savings)
        losses = s.loss_rate * stock
        shortage = max(0.0, effective_demand + losses - (stock + s.inflow))
        push!(rows, (
            scenario=s.name,
            boundary_version=s.boundary_version,
            period=period,
            stock=stock,
            shortage=shortage
        ))
        stock = bounded_update(stock, s.inflow, effective_demand, losses, s.capacity)
    end
    return rows
end

function main()
    scenarios = [
        BoundaryScenario("julia_narrow_baseline", "narrow_stock_flow", 80.0, 100.0, 8.0, 6.0, 0.015, 0.0, 60),
        BoundaryScenario("julia_policy_expanded", "policy_expanded", 80.0, 100.0, 5.0, 6.0, 0.015, 1.5, 60),
        BoundaryScenario("julia_temporal_expanded", "temporal_expanded", 70.0, 80.0, 5.0, 7.0, 0.030, 0.5, 120)
    ]

    for scenario in scenarios
        rows = simulate(scenario)
        stocks = [row.stock for row in rows]
        shortages = [row.shortage for row in rows]
        @printf("%s boundary=%s final_stock=%.3f mean_stock=%.3f total_shortage=%.3f\n",
                scenario.name, scenario.boundary_version, stocks[end], mean(stocks), sum(shortages))
    end
end

main()
