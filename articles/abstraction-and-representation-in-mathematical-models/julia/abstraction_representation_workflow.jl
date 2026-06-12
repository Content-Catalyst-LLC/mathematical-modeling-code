# Julia workflow for stock-flow representation and abstraction review.
# Dependency-light: Base and standard library only.

using Printf
using Statistics

struct StockFlowScenario
    name::String
    initial_stock::Float64
    capacity::Float64
    inflow::Float64
    demand::Float64
    loss_rate::Float64
    periods::Int
end

function bounded_update(stock, inflow, demand, losses, capacity)
    return min(capacity, max(0.0, stock + inflow - demand - losses))
end

function simulate(s::StockFlowScenario)
    stock = s.initial_stock
    rows = Vector{NamedTuple}()
    for period in 0:s.periods
        losses = s.loss_rate * stock
        shortage = max(0.0, s.demand + losses - (stock + s.inflow))
        push!(rows, (
            scenario=s.name,
            period=period,
            stock=stock,
            inflow=s.inflow,
            demand=s.demand,
            losses=losses,
            shortage=shortage
        ))
        stock = bounded_update(stock, s.inflow, s.demand, losses, s.capacity)
    end
    return rows
end

function main()
    scenarios = [
        StockFlowScenario("julia_aggregate_baseline", 80.0, 100.0, 8.0, 6.0, 0.015, 60),
        StockFlowScenario("julia_low_inflow", 80.0, 100.0, 5.0, 6.0, 0.015, 60),
        StockFlowScenario("julia_compound_stress", 70.0, 80.0, 5.0, 7.0, 0.030, 60)
    ]

    for scenario in scenarios
        rows = simulate(scenario)
        stocks = [row.stock for row in rows]
        shortages = [row.shortage for row in rows]
        @printf("%s final_stock=%.3f mean_stock=%.3f total_shortage=%.3f\n",
                scenario.name, stocks[end], mean(stocks), sum(shortages))
    end
end

main()
