# Julia workflow for mathematical modeling in an age of complexity.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct ComplexityScenario
    key::String
    scenario_name::String
    stress_level::Float64
    interdependence_level::Float64
    uncertainty_level::Float64
    resilience_score::Float64
    equity_score::Float64
    adaptability_score::Float64
end

function scenarios()
    [
        ComplexityScenario("baseline", "Baseline stress", 0.35, 0.45, 0.40, 0.72, 0.68, 0.65),
        ComplexityScenario("compound_shock", "Compound shock", 0.78, 0.70, 0.72, 0.48, 0.52, 0.55),
        ComplexityScenario("cascading_failure", "Cascading failure", 0.88, 0.86, 0.75, 0.32, 0.40, 0.42),
        ComplexityScenario("adaptive_pathway", "Adaptive pathway", 0.65, 0.68, 0.70, 0.66, 0.70, 0.82)
    ]
end

function fragility_score(s)
    0.35 * s.stress_level +
    0.30 * s.interdependence_level +
    0.25 * s.uncertainty_level +
    0.10 * (1.0 - s.adaptability_score)
end

function robust_value(s)
    f = fragility_score(s)
    0.40 * s.resilience_score +
    0.30 * s.equity_score +
    0.30 * s.adaptability_score -
    0.20 * f
end

function main()
    rows = scenarios()
    fragility = [fragility_score(s) for s in rows]
    robust = [robust_value(s) for s in rows]

    println("key,stress_level,interdependence_level,uncertainty_level,resilience_score,equity_score,adaptability_score,fragility_score,robust_value")
    for (s, f, r) in zip(rows, fragility, robust)
        @printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
                s.key, s.stress_level, s.interdependence_level, s.uncertainty_level,
                s.resilience_score, s.equity_score, s.adaptability_score, f, r)
    end

    highest_index = argmax(fragility)
    best_index = argmax(robust)
    @printf("summary,highest_fragility=%s,best_robust_value=%s,mean_fragility=%.6f,mean_robust=%.6f\n",
            rows[highest_index].scenario_name, rows[best_index].scenario_name, mean(fragility), mean(robust))
end

main()
