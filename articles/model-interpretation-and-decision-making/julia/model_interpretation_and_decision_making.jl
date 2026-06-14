# Julia workflow for model interpretation and decision-making.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct DecisionOption
    key::String
    name::String
    expected_stock::Float64
    lower_bound::Float64
    upper_bound::Float64
    burden::Float64
    consequence_if_wrong::Float64
end

function options()
    [
        DecisionOption("no_action", "No immediate action", 52.0, 38.0, 66.0, 1.0, 9.0),
        DecisionOption("monitoring", "Formal monitoring", 54.0, 42.0, 68.0, 3.0, 6.0),
        DecisionOption("moderate_intervention", "Moderate intervention", 60.0, 50.0, 72.0, 5.0, 4.0),
        DecisionOption("strong_intervention", "Strong intervention", 68.0, 58.0, 78.0, 8.0, 2.0)
    ]
end

function decision_score(option; threshold=45.0)
    crosses = option.lower_bound < threshold
    penalty = crosses ? 8.0 : 0.0
    return option.expected_stock - 0.8 * option.burden - 1.2 * option.consequence_if_wrong - penalty
end

function main()
    opts = options()
    scores = [decision_score(o) for o in opts]

    println("key,option_name,decision_score,threshold_margin,robustness_class")
    for (o, score) in zip(opts, scores)
        class = o.lower_bound >= 45.0 ? "robust" : "fragile"
        @printf("%s,%s,%.3f,%.3f,%s\n", o.key, o.name, score, o.expected_stock - 45.0, class)
    end

    best_index = argmax(scores)
    @printf("summary,best=%s,mean_score=%.3f,max_score=%.3f,min_score=%.3f\n",
            opts[best_index].name, mean(scores), maximum(scores), minimum(scores))
end

main()
