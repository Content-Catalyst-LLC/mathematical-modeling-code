# Julia workflow for model governance and accountability.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct GovernanceRiskCase
    key::String
    model_name::String
    error_risk::Float64
    uncertainty_level::Float64
    consequence_level::Float64
    scope_misuse_risk::Float64
    accountability_gap::Float64
end

function risk_cases()
    [
        GovernanceRiskCase("infrastructure_risk", "Infrastructure risk prioritization model", 0.38, 0.56, 0.82, 0.42, 0.24),
        GovernanceRiskCase("public_health_demand", "Public health demand model", 0.50, 0.68, 0.86, 0.48, 0.32),
        GovernanceRiskCase("supply_chain_resilience", "Supply chain resilience model", 0.36, 0.52, 0.65, 0.40, 0.22),
        GovernanceRiskCase("ai_triage_support", "AI-assisted triage support model", 0.62, 0.72, 0.95, 0.70, 0.55)
    ]
end

function governance_risk_score(c)
    0.20 * c.error_risk +
    0.20 * c.uncertainty_level +
    0.25 * c.consequence_level +
    0.20 * c.scope_misuse_risk +
    0.15 * c.accountability_gap
end

function review_class(score)
    if score >= 0.70
        return "escalation_required"
    elseif score >= 0.55
        return "governance_review_required"
    else
        return "standard_monitoring"
    end
end

function main()
    rows = risk_cases()
    scores = [governance_risk_score(c) for c in rows]

    println("key,error_risk,uncertainty_level,consequence_level,scope_misuse_risk,accountability_gap,governance_risk_score,review_class")
    for (c, score) in zip(rows, scores)
        @printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
                c.key, c.error_risk, c.uncertainty_level, c.consequence_level,
                c.scope_misuse_risk, c.accountability_gap, score, review_class(score))
    end

    highest_index = argmax(scores)
    @printf("summary,highest_risk=%s,mean_score=%.6f,max_score=%.6f,min_score=%.6f\n",
            rows[highest_index].model_name, mean(scores), maximum(scores), minimum(scores))
end

main()
