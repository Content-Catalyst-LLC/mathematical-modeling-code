# Julia workflow for sensitivity analysis and robustness.
# Dependency-light: Base + standard libraries only.

using Printf

struct Parameter
    name::String
    baseline::Float64
    low::Float64
    high::Float64
    label::String
end

function parameters()
    [
        Parameter("initial_stock", 80.0, 72.0, 88.0, "measurement"),
        Parameter("growth_rate", 0.08, 0.04, 0.12, "parameter"),
        Parameter("carrying_capacity", 120.0, 100.0, 140.0, "structural"),
        Parameter("extraction_rate", 0.12, 0.08, 0.18, "policy"),
        Parameter("shock_intensity", 0.03, 0.00, 0.08, "scenario")
    ]
end

function resource_projection(initial_stock, growth_rate, carrying_capacity, extraction_rate, shock_intensity; years=10)
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
    params = parameters()
    base = Dict(p.name => p.baseline for p in params)
    base_output = resource_projection(base["initial_stock"], base["growth_rate"], base["carrying_capacity"], base["extraction_rate"], base["shock_intensity"])

    println("parameter,low_output,baseline_output,high_output,range_width")
    for p in params
        values_low = copy(base)
        values_high = copy(base)
        values_low[p.name] = p.low
        values_high[p.name] = p.high

        low_output = resource_projection(values_low["initial_stock"], values_low["growth_rate"], values_low["carrying_capacity"], values_low["extraction_rate"], values_low["shock_intensity"])
        high_output = resource_projection(values_high["initial_stock"], values_high["growth_rate"], values_high["carrying_capacity"], values_high["extraction_rate"], values_high["shock_intensity"])
        width = abs(high_output - low_output)

        @printf("%s,%.6f,%.6f,%.6f,%.6f\n", p.name, low_output, base_output, high_output, width)
    end
end

main()
