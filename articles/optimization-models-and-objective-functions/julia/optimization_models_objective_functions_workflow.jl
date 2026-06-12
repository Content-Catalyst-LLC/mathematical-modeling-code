# Julia workflow for optimization models and objective functions.
# Dependency-light: Base only.

using Printf

struct Program
    name::String
    benefit::Float64
    cost::Float64
    lower::Int
    upper::Int
end

struct Scenario
    name::String
    budget::Float64
    equity_floor::Int
end

function evaluate(allocation, programs, scenario)
    total_cost = sum(allocation[i] * programs[i].cost for i in eachindex(programs))
    total_benefit = sum(allocation[i] * programs[i].benefit for i in eachindex(programs))
    equity_ok = all(x -> x >= scenario.equity_floor, allocation)
    budget_ok = total_cost <= scenario.budget
    return (total_cost=total_cost, total_benefit=total_benefit, feasible=equity_ok && budget_ok)
end

function enumerate_best(programs, scenario)
    best_benefit = -Inf
    best_allocation = Int[]
    feasible_count = 0
    candidate_count = 0

    for x1 in programs[1].lower:programs[1].upper
        for x2 in programs[2].lower:programs[2].upper
            for x3 in programs[3].lower:programs[3].upper
                for x4 in programs[4].lower:programs[4].upper
                    allocation = [x1, x2, x3, x4]
                    result = evaluate(allocation, programs, scenario)
                    candidate_count += 1
                    if result.feasible
                        feasible_count += 1
                        if result.total_benefit > best_benefit
                            best_benefit = result.total_benefit
                            best_allocation = allocation
                        end
                    end
                end
            end
        end
    end

    return (candidate_count=candidate_count, feasible_count=feasible_count, best_benefit=best_benefit, best_allocation=best_allocation)
end

function main()
    programs = [
        Program("housing", 11.0, 7.0, 0, 8),
        Program("health", 13.0, 8.0, 0, 8),
        Program("transport", 8.0, 5.0, 0, 8),
        Program("resilience", 10.0, 6.0, 0, 8)
    ]

    scenarios = [
        Scenario("julia_baseline", 75.0, 1),
        Scenario("julia_tight_budget", 55.0, 1),
        Scenario("julia_higher_floor", 75.0, 3)
    ]

    for scenario in scenarios
        result = enumerate_best(programs, scenario)
        @printf("%s candidates=%d feasible=%d best_benefit=%.2f best_allocation=%s\n",
                scenario.name, result.candidate_count, result.feasible_count, result.best_benefit, string(result.best_allocation))
    end
end

main()
