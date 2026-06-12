# Julia workflow for numerical methods for mathematical models.
# Dependency-light: Base only.

using Printf

struct SolverScenario
    name::String
    initial_stock::Float64
    growth_rate::Float64
    carrying_capacity::Float64
    extraction::Float64
    horizon::Float64
    step_size::Float64
end

function derivative(stock, growth_rate, carrying_capacity, extraction)
    return growth_rate * stock * (1.0 - stock / carrying_capacity) - extraction
end

function run_euler(scenario::SolverScenario)
    stock = scenario.initial_stock
    steps = Int(round(scenario.horizon / scenario.step_size))

    for _ in 1:steps
        stock = stock + scenario.step_size * derivative(
            stock,
            scenario.growth_rate,
            scenario.carrying_capacity,
            scenario.extraction
        )
        stock = max(0.0, stock)
    end

    return stock
end

function main()
    scenarios = [
        SolverScenario("resource_dynamics", 70.0, 0.18, 100.0, 6.0, 50.0, 1.0),
        SolverScenario("resource_dynamics", 70.0, 0.18, 100.0, 6.0, 50.0, 0.5),
        SolverScenario("resource_dynamics", 70.0, 0.18, 100.0, 6.0, 50.0, 0.25),
        SolverScenario("resource_dynamics", 70.0, 0.18, 100.0, 6.0, 50.0, 0.1)
    ]

    finest = run_euler(scenarios[end])
    for scenario in scenarios
        final_stock = run_euler(scenario)
        @printf("h=%.3f final_stock=%.6f difference_from_finest=%.6f\n",
                scenario.step_size, final_stock, abs(final_stock - finest))
    end
end

main()
