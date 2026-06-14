# Julia workflow for mathematical modeling in policy and public systems.
# Dependency-light: Base + standard libraries only.

using Printf
using Statistics

struct PolicyOption
    key::String
    option_name::String
    projected_benefit::Float64
    total_cost::Float64
    feasibility::Float64
    equity_score::Float64
    uncertainty_width::Float64
    public_risk::Float64
end

function policy_options()
    [
        PolicyOption("baseline", "Maintain current services", 42.0, 18.0, 0.86, 0.52, 18.0, 0.42),
        PolicyOption("targeted_prevention", "Targeted prevention program", 68.0, 32.0, 0.74, 0.78, 22.0, 0.30),
        PolicyOption("broad_expansion", "Broad service expansion", 81.0, 49.0, 0.58, 0.69, 28.0, 0.34),
        PolicyOption("adaptive_pathway", "Adaptive pathway with monitoring triggers", 73.0, 38.0, 0.70, 0.82, 16.0, 0.24)
    ]
end

function public_value_score(option; budget_limit=40.0)
    budget_violation = option.total_cost > budget_limit
    uncertainty_penalty = 0.22 * option.uncertainty_width
    risk_penalty = 30.0 * option.public_risk
    feasibility_bonus = 18.0 * option.feasibility
    equity_bonus = 24.0 * option.equity_score
    budget_penalty = budget_violation ? 14.0 : 0.0
    return option.projected_benefit + feasibility_bonus + equity_bonus - option.total_cost - uncertainty_penalty - risk_penalty - budget_penalty
end

function main()
    options = policy_options()
    scores = [public_value_score(option) for option in options]

    println("key,projected_benefit,total_cost,equity_score,public_risk,public_value_score,budget_violation")
    for (option, score) in zip(options, scores)
        budget_violation = option.total_cost > 40.0
        @printf("%s,%.3f,%.3f,%.3f,%.3f,%.6f,%s\n",
                option.key, option.projected_benefit, option.total_cost, option.equity_score, option.public_risk, score, string(budget_violation))
    end

    best_index = argmax(scores)
    @printf("summary,best=%s,mean_score=%.6f,max_score=%.6f,min_score=%.6f\n",
            options[best_index].option_name, mean(scores), maximum(scores), minimum(scores))
end

main()
