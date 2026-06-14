# Julia workflow for limits, failure, and the ethics of modeling.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct ModelRiskCase
    key::String
    model_name::String
    intended_use::String
    severity::Float64
    likelihood::Float64
    detectability_gap::Float64
    uncertainty_level::Float64
    equity_concern::Float64
    accountability_gap::Float64
end

function risk_cases()
    [
        ModelRiskCase("exploratory_model", "Exploratory planning model", "learning and scenario discussion", 0.35, 0.35, 0.25, 0.60, 0.30, 0.25),
        ModelRiskCase("allocation_model", "Resource allocation model", "prioritizing scarce resources", 0.85, 0.55, 0.55, 0.65, 0.75, 0.70),
        ModelRiskCase("public_dashboard", "Public risk dashboard", "communicating population risk", 0.70, 0.50, 0.45, 0.80, 0.55, 0.60),
        ModelRiskCase("automated_score", "Automated scoring model", "triggering institutional action", 0.90, 0.60, 0.70, 0.60, 0.80, 0.85)
    ]
end

function ethical_risk_score(c)
    1.8 * c.severity +
    1.3 * c.likelihood +
    1.2 * c.detectability_gap +
    1.1 * c.uncertainty_level +
    1.5 * c.equity_concern +
    1.6 * c.accountability_gap
end

function main()
    rows = risk_cases()
    scores = [ethical_risk_score(c) for c in rows]

    println("key,severity,likelihood,detectability_gap,uncertainty_level,equity_concern,accountability_gap,ethical_risk_score")
    for (c, score) in zip(rows, scores)
        @printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
                c.key, c.severity, c.likelihood, c.detectability_gap,
                c.uncertainty_level, c.equity_concern, c.accountability_gap, score)
    end

    best_index = argmax(scores)
    @printf("summary,highest_risk=%s,mean_score=%.6f,max_score=%.6f,min_score=%.6f\n",
            rows[best_index].model_name, mean(scores), maximum(scores), minimum(scores))
end

main()
