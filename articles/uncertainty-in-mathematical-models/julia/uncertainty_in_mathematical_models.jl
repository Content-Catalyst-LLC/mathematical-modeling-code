# Julia workflow for uncertainty in mathematical models.
# Dependency-light: Base + standard libraries only.

using Printf
using Random
using Statistics

struct UncertainParameter
    name::String
    low::Float64
    baseline::Float64
    high::Float64
    uncertainty_type::String
end

function parameters()
    [
        UncertainParameter("initial_stock", 72.0, 80.0, 88.0, "measurement"),
        UncertainParameter("growth_rate", 0.04, 0.08, 0.12, "parameter"),
        UncertainParameter("carrying_capacity", 100.0, 120.0, 140.0, "structural"),
        UncertainParameter("extraction_rate", 0.08, 0.12, 0.18, "scenario"),
        UncertainParameter("shock_intensity", 0.00, 0.03, 0.08, "aleatory")
    ]
end

function projection(initial_stock, growth_rate, carrying_capacity, extraction_rate, shock_intensity; years=10)
    stock = initial_stock
    for _ in 1:years
        growth = growth_rate * stock * (1.0 - stock / carrying_capacity)
        extraction = extraction_rate * stock
        shock = shock_intensity * stock
        stock = max(0.0, stock + growth - extraction - shock)
    end
    return stock
end

function main()
    Random.seed!(42)
    params = parameters()
    outputs = Float64[]
    threshold_count = 0
    n = 1000

    for _ in 1:n
        values = Dict(p.name => rand() * (p.high - p.low) + p.low for p in params)
        y = projection(values["initial_stock"], values["growth_rate"], values["carrying_capacity"], values["extraction_rate"], values["shock_intensity"])
        push!(outputs, y)
        if y < 45.0
            threshold_count += 1
        end
    end

    sorted_outputs = sort(outputs)
    p05 = sorted_outputs[Int(round(0.05 * (n - 1))) + 1]
    p95 = sorted_outputs[Int(round(0.95 * (n - 1))) + 1]

    @printf("mean=%.6f median=%.6f p05=%.6f p95=%.6f threshold_probability=%.6f\n",
            mean(outputs), median(outputs), p05, p95, threshold_count / n)
end

main()
