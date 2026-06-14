# Julia workflow for AI-assisted modeling and human judgment.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct HumanJudgmentCase
    key::String
    judgment_point::String
    decision_context::String
    evidence_strength::Float64
    uncertainty_level::Float64
    consequence_level::Float64
    automation_bias_risk::Float64
    accountability_clarity::Float64
end

function judgment_cases()
    [
        HumanJudgmentCase("problem_frame", "problem framing", "public infrastructure stress model", 0.72, 0.58, 0.80, 0.45, 0.70),
        HumanJudgmentCase("data_fit", "data fitness judgment", "using administrative records", 0.62, 0.66, 0.75, 0.50, 0.65),
        HumanJudgmentCase("model_use", "approved use decision", "moving from exploratory to decision support", 0.68, 0.70, 0.88, 0.72, 0.55),
        HumanJudgmentCase("public_summary", "communication approval", "publishing model results", 0.76, 0.62, 0.82, 0.60, 0.72)
    ]
end

function judgment_risk_score(c)
    0.25 * (1.0 - c.evidence_strength) +
    0.25 * c.uncertainty_level +
    0.25 * c.consequence_level +
    0.15 * c.automation_bias_risk +
    0.10 * (1.0 - c.accountability_clarity)
end

function main()
    rows = judgment_cases()
    scores = [judgment_risk_score(c) for c in rows]

    println("key,evidence_strength,uncertainty_level,consequence_level,automation_bias_risk,accountability_clarity,judgment_risk_score")
    for (c, score) in zip(rows, scores)
        @printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
                c.key, c.evidence_strength, c.uncertainty_level, c.consequence_level,
                c.automation_bias_risk, c.accountability_clarity, score)
    end

    highest_index = argmax(scores)
    @printf("summary,highest_risk=%s,mean_score=%.6f,max_score=%.6f,min_score=%.6f\n",
            rows[highest_index].judgment_point, mean(scores), maximum(scores), minimum(scores))
end

main()
