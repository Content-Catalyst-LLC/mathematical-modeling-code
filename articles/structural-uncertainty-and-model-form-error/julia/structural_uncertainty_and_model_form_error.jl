# Julia workflow for structural uncertainty and model-form comparison.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct ModelForm
    key::String
    family::String
end

function forms()
    [
        ModelForm("linear_decline", "algebraic"),
        ModelForm("proportional_decline", "dynamic"),
        ModelForm("logistic_recovery", "dynamic"),
        ModelForm("threshold_shift", "piecewise")
    ]
end

function simulate_model(form_key; years=10)
    stock = 80.0
    carrying_capacity = 120.0
    extraction_rate = 0.12
    growth_rate = 0.08
    fixed_loss = 5.8
    critical_threshold = 55.0

    for _ in 1:years
        if form_key == "linear_decline"
            stock = max(0.0, stock - fixed_loss)
        elseif form_key == "proportional_decline"
            stock = max(0.0, stock - extraction_rate * stock)
        elseif form_key == "logistic_recovery"
            growth = growth_rate * stock * (1.0 - stock / carrying_capacity)
            extraction = extraction_rate * stock
            stock = max(0.0, stock + growth - extraction)
        elseif form_key == "threshold_shift"
            if stock < critical_threshold
                stock = max(0.0, stock - 1.6 * extraction_rate * stock)
            else
                stock = max(0.0, stock - extraction_rate * stock)
            end
        else
            error("Unknown model form")
        end
    end
    return stock
end

function main()
    fs = forms()
    outputs = [simulate_model(f.key) for f in fs]
    threshold_flags = [y < 45.0 for y in outputs]
    spread = maximum(outputs) - minimum(outputs)

    println("model_form,model_family,projected_stock,below_threshold")
    for (f, y, flag) in zip(fs, outputs, threshold_flags)
        @printf("%s,%s,%.6f,%s\n", f.key, f.family, y, string(flag))
    end

    @printf("summary,mean=%.6f,min=%.6f,max=%.6f,structural_spread=%.6f,threshold_disagreement=%s\n",
            mean(outputs), minimum(outputs), maximum(outputs), spread, string(length(unique(threshold_flags)) > 1))
end

main()
