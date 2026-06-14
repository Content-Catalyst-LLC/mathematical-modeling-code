using Printf
using Statistics

struct FutureModelingDirection
    key::String
    complexity_relevance::Float64
    technical_maturity::Float64
    governance_need::Float64
    uncertainty_pressure::Float64
    human_judgment_need::Float64
end

function directions()
    [
        FutureModelingDirection("hybrid_models", 0.88, 0.70, 0.74, 0.72, 0.80),
        FutureModelingDirection("ai_assistance", 0.82, 0.78, 0.90, 0.76, 0.92),
        FutureModelingDirection("digital_twins", 0.86, 0.75, 0.88, 0.70, 0.84),
        FutureModelingDirection("uncertainty_workflows", 0.90, 0.72, 0.82, 0.92, 0.86),
        FutureModelingDirection("participatory_modeling", 0.78, 0.62, 0.86, 0.68, 0.94)
    ]
end

function priority(d)
    0.25*d.complexity_relevance + 0.20*d.technical_maturity + 0.20*d.governance_need + 0.20*d.uncertainty_pressure + 0.15*d.human_judgment_need
end

function review_class(d)
    p = priority(d)
    if d.governance_need >= 0.85 || d.human_judgment_need >= 0.90
        "governance_priority"
    elseif d.uncertainty_pressure >= 0.85
        "uncertainty_priority"
    elseif p >= 0.78
        "strategic_priority"
    else
        "monitor"
    end
end

rows = directions()
scores = [priority(d) for d in rows]
println("key,complexity_relevance,technical_maturity,governance_need,uncertainty_pressure,human_judgment_need,future_priority_score,review_class")
for (d, s) in zip(rows, scores)
    @printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n", d.key, d.complexity_relevance, d.technical_maturity, d.governance_need, d.uncertainty_pressure, d.human_judgment_need, s, review_class(d))
end
@printf("summary,mean_score=%.6f,max_score=%.6f,min_score=%.6f\n", mean(scores), maximum(scores), minimum(scores))
