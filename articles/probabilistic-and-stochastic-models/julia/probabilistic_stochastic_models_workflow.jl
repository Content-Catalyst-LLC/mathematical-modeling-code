# Julia workflow for probabilistic and stochastic models.
# Dependency-light: Base, Random, Statistics only.

using Random
using Statistics
using Printf

struct RiskScenario
    name::String
    demand_mu::Float64
    demand_sigma::Float64
    supply_mean::Float64
    supply_sd::Float64
    reserve::Float64
    simulations::Int
    seed::Int
end

function quantile_simple(values, p)
    sorted_values = sort(values)
    index = clamp(round(Int, p * (length(sorted_values) - 1)) + 1, 1, length(sorted_values))
    return sorted_values[index]
end

function simulate(s::RiskScenario)
    Random.seed!(s.seed)
    shortages = Float64[]

    for _ in 1:s.simulations
        demand = exp(s.demand_mu + s.demand_sigma * randn())
        supply = max(0.0, s.supply_mean + s.supply_sd * randn())
        shortage = max(0.0, demand - (supply + s.reserve))
        push!(shortages, shortage)
    end

    shortage_probability = count(x -> x > 0.0, shortages) / s.simulations
    return (
        shortage_probability=shortage_probability,
        expected_shortage=mean(shortages),
        shortage_q95=quantile_simple(shortages, 0.95),
        max_shortage=maximum(shortages)
    )
end

function main()
    scenarios = [
        RiskScenario("julia_baseline", 4.50, 0.25, 95.0, 8.0, 5.0, 5000, 101),
        RiskScenario("julia_high_variability", 4.50, 0.45, 95.0, 12.0, 5.0, 5000, 102),
        RiskScenario("julia_low_reserve", 4.50, 0.25, 95.0, 8.0, 0.0, 5000, 103)
    ]

    for scenario in scenarios
        result = simulate(scenario)
        @printf("%s shortage_probability=%.4f expected_shortage=%.4f q95=%.4f max_shortage=%.4f\n",
                scenario.name, result.shortage_probability, result.expected_shortage, result.shortage_q95, result.max_shortage)
    end
end

main()
