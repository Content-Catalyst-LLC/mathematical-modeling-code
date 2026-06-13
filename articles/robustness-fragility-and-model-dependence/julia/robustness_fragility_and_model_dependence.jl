# Julia workflow for robustness, fragility, and model dependence.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct ModelScenario
    key::String
    model_form::String
    scenario::String
    extraction_multiplier::Float64
    shock::Float64
end

function scenarios()
    [
        ModelScenario("linear_baseline", "linear_decline", "baseline", 1.0, 0.00),
        ModelScenario("linear_stress", "linear_decline", "stress", 1.25, 0.05),
        ModelScenario("dynamic_baseline", "logistic_recovery", "baseline", 1.0, 0.00),
        ModelScenario("dynamic_stress", "logistic_recovery", "stress", 1.25, 0.05),
        ModelScenario("threshold_baseline", "threshold_shift", "baseline", 1.0, 0.00),
        ModelScenario("threshold_stress", "threshold_shift", "stress", 1.25, 0.05)
    ]
end

function simulate(form, extraction_multiplier, shock; years=10)
    stock = 80.0
    carrying_capacity = 120.0
    growth_rate = 0.08
    extraction_rate = 0.12 * extraction_multiplier
    fixed_loss = 5.8 * extraction_multiplier
    critical_threshold = 55.0

    for _ in 1:years
        if form == "linear_decline"
            stock = max(0.0, stock - fixed_loss - shock * stock)
        elseif form == "logistic_recovery"
            growth = growth_rate * stock * (1.0 - stock / carrying_capacity)
            extraction = extraction_rate * stock
            stock = max(0.0, stock + growth - extraction - shock * stock)
        elseif form == "threshold_shift"
            if stock < critical_threshold
                stock = max(0.0, stock - 1.6 * extraction_rate * stock - shock * stock)
            else
                stock = max(0.0, stock - extraction_rate * stock - shock * stock)
            end
        else
            error("Unknown model form")
        end
    end
    return stock
end

function main()
    items = scenarios()
    outputs = Float64[]
    threshold_flags = Bool[]

    println("key,model_form,scenario,projected_stock,below_threshold,fragility_class")
    for item in items
        y = simulate(item.model_form, item.extraction_multiplier, item.shock)
        push!(outputs, y)
        flag = y < 45.0
        push!(threshold_flags, flag)
        fragility_class = abs(y - 45.0) <= 5.0 ? "fragile" : "stable_margin"
        @printf("%s,%s,%s,%.6f,%s,%s\n", item.key, item.model_form, item.scenario, y, string(flag), fragility_class)
    end

    @printf("summary,mean=%.6f,min=%.6f,max=%.6f,robustness_spread=%.6f,threshold_disagreement=%s\n",
            mean(outputs), minimum(outputs), maximum(outputs), maximum(outputs)-minimum(outputs), string(length(unique(threshold_flags)) > 1))
end

main()
