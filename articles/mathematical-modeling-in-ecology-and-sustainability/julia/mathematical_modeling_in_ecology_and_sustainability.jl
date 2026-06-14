# Julia workflow for mathematical modeling in ecology and sustainability.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct ResourceScenario
    key::String
    scenario_name::String
    initial_stock::Float64
    growth_rate::Float64
    carrying_capacity::Float64
    extraction::Float64
    climate_stress::Float64
    years::Int
    minimum_stock::Float64
end

function scenarios()
    [
        ResourceScenario("baseline", "Baseline managed use", 420.0, 0.24, 800.0, 36.0, 0.04, 25, 250.0),
        ResourceScenario("high_extraction", "High extraction pressure", 420.0, 0.24, 800.0, 64.0, 0.04, 25, 250.0),
        ResourceScenario("climate_stress", "Climate stress with lower regeneration", 420.0, 0.24, 800.0, 42.0, 0.22, 25, 250.0),
        ResourceScenario("restoration_pathway", "Restoration and reduced extraction", 420.0, 0.28, 860.0, 24.0, 0.03, 25, 250.0),
        ResourceScenario("adaptive_management", "Adaptive use with monitoring trigger", 420.0, 0.25, 820.0, 32.0, 0.08, 25, 250.0)
    ]
end

function simulate_final(s)
    stock = s.initial_stock
    effective_growth = s.growth_rate * (1.0 - s.climate_stress)
    min_stock_seen = stock
    min_margin_seen = stock - s.minimum_stock

    for _ in 1:s.years
        regeneration = effective_growth * stock * (1.0 - stock / s.carrying_capacity)
        stock = max(0.0, stock + regeneration - s.extraction)
        min_stock_seen = min(min_stock_seen, stock)
        min_margin_seen = min(min_margin_seen, stock - s.minimum_stock)
    end

    return stock, min_stock_seen, min_margin_seen
end

function main()
    items = scenarios()
    finals = Float64[]

    println("key,final_stock,minimum_observed_stock,minimum_resilience_margin,threshold_breach")
    for s in items
        final_stock, min_stock_seen, min_margin_seen = simulate_final(s)
        push!(finals, final_stock)
        threshold_breach = min_stock_seen < s.minimum_stock
        @printf("%s,%.6f,%.6f,%.6f,%s\n",
                s.key, final_stock, min_stock_seen, min_margin_seen, string(threshold_breach))
    end

    @printf("summary,mean_final_stock=%.6f,min_final_stock=%.6f,max_final_stock=%.6f,scenario_spread=%.6f\n",
            mean(finals), minimum(finals), maximum(finals), maximum(finals) - minimum(finals))
end

main()
