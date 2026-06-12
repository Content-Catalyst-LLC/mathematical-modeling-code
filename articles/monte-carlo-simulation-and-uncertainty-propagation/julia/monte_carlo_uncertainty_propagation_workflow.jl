# Julia workflow for Monte Carlo simulation and uncertainty propagation.
# Dependency-light: Base + standard libraries only.

using Random
using Printf
using Statistics

struct Scenario
    name::String
    initial_stock_min::Float64
    initial_stock_max::Float64
    growth_rate_min::Float64
    growth_rate_max::Float64
    extraction_min::Float64
    extraction_max::Float64
    shock_probability_min::Float64
    shock_probability_max::Float64
    shock_fraction::Float64
    carrying_capacity::Float64
    steps::Int
    replications::Int
    threshold::Float64
    seed::Int
end

function run_once(s::Scenario, rng)
    stock = rand(rng) * (s.initial_stock_max - s.initial_stock_min) + s.initial_stock_min
    growth_rate = rand(rng) * (s.growth_rate_max - s.growth_rate_min) + s.growth_rate_min
    extraction = rand(rng) * (s.extraction_max - s.extraction_min) + s.extraction_min
    shock_probability = rand(rng) * (s.shock_probability_max - s.shock_probability_min) + s.shock_probability_min

    for _ in 1:s.steps
        growth = growth_rate * stock * (1.0 - stock / s.carrying_capacity)
        shock = rand(rng) < shock_probability ? stock * s.shock_fraction : 0.0
        stock = max(0.0, stock + growth - extraction - shock)
    end

    return stock
end

function main()
    scenarios = [
        Scenario("baseline_uncertainty", 65.0, 75.0, 0.14, 0.22, 5.0, 8.0, 0.02, 0.08, 0.12, 100.0, 50, 1000, 10.0, 20260612),
        Scenario("stress_uncertainty", 60.0, 75.0, 0.10, 0.20, 7.0, 11.0, 0.08, 0.18, 0.22, 100.0, 50, 1000, 10.0, 20260613)
    ]

    for s in scenarios
        rng = MersenneTwister(s.seed)
        values = [run_once(s, rng) for _ in 1:s.replications]
        depletion_probability = sum(value <= s.threshold for value in values) / length(values)
        @printf("%s mean_final_stock=%.4f median=%.4f p05=%.4f p95=%.4f depletion_probability=%.4f\n",
                s.name, mean(values), median(values), quantile(values, 0.05), quantile(values, 0.95), depletion_probability)
    end
end

main()
