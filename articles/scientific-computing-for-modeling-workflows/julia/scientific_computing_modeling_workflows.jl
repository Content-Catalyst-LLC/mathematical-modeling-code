# Julia workflow for scientific computing for modeling workflows.
# Dependency-light: Base + standard libraries only.

using Random
using Printf
using Dates

struct ResourceScenario
    name::String
    initial_stock::Float64
    growth_rate::Float64
    carrying_capacity::Float64
    extraction::Float64
    shock_probability::Float64
    shock_fraction::Float64
    steps::Int
    seed::Int
end

function simulate(s::ResourceScenario)
    rng = MersenneTwister(s.seed)
    stock = s.initial_stock
    min_stock = stock

    for _ in 1:s.steps
        growth = s.growth_rate * stock * (1.0 - stock / s.carrying_capacity)
        shock = rand(rng) < s.shock_probability ? stock * s.shock_fraction : 0.0
        stock = max(0.0, stock + growth - s.extraction - shock)
        min_stock = min(min_stock, stock)
    end

    return stock, min_stock
end

function main()
    scenarios = [
        ResourceScenario("baseline", 70.0, 0.18, 100.0, 6.0, 0.05, 0.10, 50, 20260612),
        ResourceScenario("stress", 70.0, 0.15, 100.0, 9.0, 0.12, 0.20, 50, 20260613),
        ResourceScenario("recovery_policy", 70.0, 0.18, 100.0, 5.0, 0.05, 0.10, 50, 20260614)
    ]

    println("scientific_computing_workflow_run=", Dates.now())

    for s in scenarios
        final_stock, min_stock = simulate(s)
        @printf("%s final_stock=%.4f minimum_stock=%.4f seed=%d\n",
                s.name, final_stock, min_stock, s.seed)
    end
end

main()
