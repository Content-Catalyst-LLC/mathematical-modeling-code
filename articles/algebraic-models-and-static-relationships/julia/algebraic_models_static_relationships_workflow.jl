# Julia workflow for algebraic models and static relationships.
# Dependency-light: Base and standard library only.

using Printf

struct AllocationScenario
    name::String
    budget::Float64
    cost_a::Float64
    cost_b::Float64
    benefit_a::Float64
    benefit_b::Float64
    allocation_a::Float64
    allocation_b::Float64
    capacity_a::Float64
    capacity_b::Float64
end

function evaluate(s::AllocationScenario)
    total_cost = s.cost_a * s.allocation_a + s.cost_b * s.allocation_b
    total_benefit = s.benefit_a * s.allocation_a + s.benefit_b * s.allocation_b
    budget_slack = s.budget - total_cost
    capacity_slack_a = s.capacity_a - s.allocation_a
    capacity_slack_b = s.capacity_b - s.allocation_b
    feasible = budget_slack >= 0 && capacity_slack_a >= 0 && capacity_slack_b >= 0
    benefit_per_cost = total_cost > 0 ? total_benefit / total_cost : 0.0
    return (total_cost, total_benefit, benefit_per_cost, budget_slack, feasible)
end

function main()
    scenarios = [
        AllocationScenario("julia_balanced", 100.0, 4.0, 5.0, 8.0, 11.0, 10.0, 8.0, 20.0, 15.0),
        AllocationScenario("julia_budget_stress", 80.0, 4.0, 5.0, 8.0, 11.0, 12.0, 8.0, 20.0, 15.0),
        AllocationScenario("julia_capacity_stress", 120.0, 4.0, 5.0, 8.0, 11.0, 25.0, 5.0, 20.0, 15.0)
    ]

    for scenario in scenarios
        total_cost, total_benefit, benefit_per_cost, slack, feasible = evaluate(scenario)
        @printf("%s total_cost=%.3f total_benefit=%.3f benefit_per_cost=%.3f budget_slack=%.3f feasible=%s\n",
                scenario.name, total_cost, total_benefit, benefit_per_cost, slack, feasible)
    end
end

main()
