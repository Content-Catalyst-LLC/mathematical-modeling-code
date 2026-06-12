# Julia workflow for functional relationship and structure comparison.
# Dependency-light: Base and standard library only.

using Printf
using Random
using Statistics

struct StructureScenario
    name::String
    structure::String
    initial_stock::Float64
    capacity::Float64
    inflow::Float64
    demand::Float64
    loss_rate::Float64
    feedback_strength::Float64
    periods::Int
end

function simulate(s::StructureScenario; seed=42)
    Random.seed!(seed)
    stock = s.initial_stock
    demand = s.demand
    rows = Vector{NamedTuple}()

    for period in 0:s.periods
        inflow = s.inflow
        if s.structure == "stochastic"
            inflow = s.inflow * exp(randn() * 0.18)
        end

        losses = s.loss_rate * stock
        raw_next = stock + inflow - demand - losses
        shortage = max(0.0, -raw_next)
        overflow = max(0.0, raw_next - s.capacity)

        next_stock = raw_next
        if s.structure in ["constrained", "feedback", "stochastic", "threshold"]
            next_stock = min(s.capacity, max(0.0, raw_next))
        end

        push!(rows, (
            scenario=s.name,
            structure=s.structure,
            period=period,
            stock=stock,
            shortage=shortage,
            overflow=overflow
        ))

        if s.structure == "feedback"
            demand = max(0.0, demand - s.feedback_strength * shortage)
        end

        stock = next_stock
    end

    return rows
end

function main()
    scenarios = [
        StructureScenario("julia_linear", "linear", 80.0, 100.0, 8.0, 6.0, 0.015, 0.0, 60),
        StructureScenario("julia_constrained", "constrained", 80.0, 100.0, 8.0, 6.0, 0.015, 0.0, 60),
        StructureScenario("julia_feedback", "feedback", 40.0, 60.0, 3.0, 7.0, 0.050, 0.20, 60),
        StructureScenario("julia_stochastic", "stochastic", 70.0, 100.0, 6.0, 6.0, 0.020, 0.0, 60)
    ]

    for scenario in scenarios
        rows = simulate(scenario)
        stocks = [row.stock for row in rows]
        shortages = [row.shortage for row in rows]
        @printf("%s structure=%s final_stock=%.3f mean_stock=%.3f total_shortage=%.3f\n",
                scenario.name, scenario.structure, stocks[end], mean(stocks), sum(shortages))
    end
end

main()
