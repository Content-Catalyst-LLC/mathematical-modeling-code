# Julia workflow for communicating model uncertainty.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct CommunicationRecord
    key::String
    layer::String
    audience::String
    status::String
end

function records()
    [
        CommunicationRecord("central_result", "result", "decision_maker", "active"),
        CommunicationRecord("uncertainty_range", "uncertainty", "public", "review"),
        CommunicationRecord("threshold_risk", "decision_threshold", "decision_maker", "review"),
        CommunicationRecord("structural_limit", "model_limit", "technical_reviewer", "review"),
        CommunicationRecord("use_limit", "governance", "future_user", "review")
    ]
end

function priority(record)
    score = record.status == "active" ? 1.0 : 5.0
    text = lowercase(record.layer * " " * record.audience)
    for term in ["threshold", "decision", "limit", "public", "governance", "uncertainty"]
        if occursin(term, text)
            score += 1.0
        end
    end
    return score
end

function main()
    rs = records()
    scores = [priority(r) for r in rs]

    println("key,communication_layer,audience,status,communication_priority")
    for (r, s) in zip(rs, scores)
        @printf("%s,%s,%s,%s,%.3f\n", r.key, r.layer, r.audience, r.status, s)
    end

    @printf("summary,mean_priority=%.3f,max_priority=%.3f,records=%d\n", mean(scores), maximum(scores), length(rs))
end

main()
