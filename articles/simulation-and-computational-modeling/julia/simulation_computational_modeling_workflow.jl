# Julia workflow for simulation and computational modeling.
# Dependency-light: Base only.

using Random
using Printf
using Statistics

struct Scenario
    name::String
    initial_stock::Float64
    growth_rate::Float64
    carrying_capacity::Float64
    extraction::Float64
    shock_probability::Float64
    shock_fraction::Float64
    steps::Int
    replications::Int
end

function extraction_for_step(scenario::Scenario, stock::Float64)
    if scenario.name == "adaptive_policy" && stock < 40.0
        return scenario.extraction * 0.35
    end
    return scenario.extraction
end

function simulate(scenario::Scenario, seed::Int)
    rng = MersenneTwister(seed)
    stock = scenario.initial_stock

    for _ in 1:scenario.steps
        growth = scenario.growth_rate * stock * (1.0 - stock / scenario.carrying_capacity)
        extraction = extraction_for_step(scenario, stock)
        shock = rand(rng) < scenario.shock_probability ? stock * scenario.shock_fraction : 0.0
        stock = max(0.0, stock + growth - extraction - shock)
    end

    return stock
end

function main()
    scenarios = [
        Scenario("baseline", 70.0, 0.18, 100.0, 6.0, 0.05, 0.10, 50, 60),
        Scenario("high_extraction", 70.0, 0.18, 100.0, 10.0, 0.05, 0.10, 50, 60),
        Scenario("adaptive_policy", 70.0, 0.18, 100.0, 6.0, 0.05, 0.10, 50, 60),
        Scenario("shock_stress", 70.0, 0.18, 100.0, 6.0, 0.15, 0.22, 50, 60)
    ]

    for scenario in scenarios
        values = [simulate(scenario, seed) for seed in 1:scenario.replications]
        depletion_probability = sum(value <= 5.0 for value in values) / length(values)
        @printf("%s mean_final_stock=%.4f min=%.4f max=%.4f depletion_probability=%.4f\n",
                scenario.name, mean(values), minimum(values), maximum(values), depletion_probability)
    end
end

main()
